import asyncpg
from asyncpg import Pool

from config.settings import settings


class Database:
    """
    API for interaction with the database.
    """

    def __init__(self):
        self.connection_pool: Pool | None = None

    async def create_connection_pool(self) -> Pool:
        """
        Creates a connection pool and returns it.
        """
        self.connection_pool = await asyncpg.create_pool(
            host=settings.POSTGRES_HOST, port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER, password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB
        )
        return self.connection_pool

    async def close_connection_pool(self):
        """
        Attempts to close all connections in the pool.
        """
        return await self.connection_pool.close()
