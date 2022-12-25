import asyncio

import pytest
import pytest_asyncio
from asyncpg import Connection

from database.db import Database
from elastic.client import ElasticsearchClient


@pytest_asyncio.fixture
async def es_client() -> ElasticsearchClient:
    client = ElasticsearchClient()
    yield client
    await client.es.close()


@pytest_asyncio.fixture
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
        query={"match_all": {}}
    )
