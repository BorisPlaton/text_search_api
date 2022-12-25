import asyncio
import random
import string
from datetime import datetime
from typing import NamedTuple

import pytest
import pytest_asyncio
from asyncpg import Connection, Record
from elasticsearch import AsyncElasticsearch

from database.db import Database
from elastic.client import ElasticsearchClient


class CreatedDocument(NamedTuple):
    iD: int
    text: str


@pytest.fixture
def add_doc_to_index(es: AsyncElasticsearch):
    async def inner(doc_id: int = None, text: str = None) -> CreatedDocument:
        doc_id = doc_id or random.randint(1, 1000)
        text = text or ''.join(random.choices(string.ascii_letters, k=random.randint(10, 100)))
        await es.index(
            index='documents',
            document={
                'iD': doc_id,
                'text': text
            },
            refresh=True
        )
        return CreatedDocument(iD=doc_id, text=text)

    return inner


@pytest_asyncio.fixture
async def es_client() -> ElasticsearchClient:
    client = ElasticsearchClient()
    yield client
    await client.es.close()


@pytest.fixture
def es(es_client) -> AsyncElasticsearch:
    return es_client.es


@pytest.fixture
def add_document(conn, doc_columns):
    async def inner(columns: list = None) -> Record:
        data = columns or doc_columns()
        return await conn.fetchrow(
            """
            INSERT INTO document(rubrics, text, created_date)
            VALUES
                ($1, $2, $3)
            RETURNING *;
            """, *data
        )

    return inner


@pytest.fixture
def doc_columns():
    return lambda: (
        [f'rubric{i}' for i in range(random.randint(1, 5))],
        ''.join(random.choices(string.ascii_letters, k=random.randint(5, 10))),
        datetime.now(),
    )


@pytest_asyncio.fixture(scope='session')
async def conn() -> Connection:
    return await Database().connect()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def db_lifecycle():
    db = Database()
    db.migrations.migrate()
    yield
    connection = await Database().connect()
    await connection.execute(
        """DROP TABLE IF EXISTS document, _yoyo_log, _yoyo_migration, _yoyo_version, yoyo_lock;"""
    )
    await connection.close()
    db.migrations.migrate()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def es_client_lifecycle():
    client = ElasticsearchClient()
    await client.create_indices()
    yield
    await client.es.indices.delete(index='documents')
    await client.create_indices()
    await client.es.transport.close()


@pytest_asyncio.fixture(autouse=True)
async def clean_tables(conn):
    await conn.execute("TRUNCATE document;")


@pytest_asyncio.fixture(autouse=True)
async def clean_indices(es_client):
    await es_client.es.delete_by_query(
        index=[index.name for index in es_client.indices],
        query={"match_all": {}},
        refresh=True
    )
