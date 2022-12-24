import pytest
import pytest_asyncio

from database.db import Database
from elastic.client import ElasticsearchClient


@pytest.fixture(scope='session', autouse=True)
async def database():
    async def truncate_tables():
        await db.connection_pool.execute("TRUNCATE document;")

    db = Database()
    db.migrations.migrate()
    await db.create_connection_pool()
    await truncate_tables()
    yield
    await truncate_tables()
    await db.close_connection_pool()


@pytest.fixture(scope='session', autouse=True)
async def es():
    client = ElasticsearchClient()
    await client.create_indices()
    yield
    await client.es.transport.close()


@pytest_asyncio.fixture(autouse=True)
async def es_client() -> ElasticsearchClient:
    client = ElasticsearchClient()
    yield client
    await client.es.delete_by_query(
        index=[index.name for index in client.indices],
        query={"match_all": {}}
    )
    await client.es.close()
