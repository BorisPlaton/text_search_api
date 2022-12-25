import asyncpg
from asyncpg import Pool, Connection

from config.settings import settings
from database.migrations import DBMigrations


class Database:
    """
    API for interaction with the database.
    """

    def __init__(self):
        self.credentials = {
            'host': settings.POSTGRES_HOST,
            'port': settings.POSTGRES_PORT,
            'user': settings.POSTGRES_USER,
            'password': settings.POSTGRES_PASSWORD,
            'database': settings.POSTGRES_DB
        }
        self.connection_pool: Pool | None = None
        self.migrations = DBMigrations()

    async def create_connection_pool(self) -> Pool:
        """
        Creates a connection pool and returns it.
        """
        self.connection_pool = await asyncpg.create_pool(**self.credentials)
        return self.connection_pool

    async def close_connection_pool(self):
        """
        Attempts to close all connections in the pool.
        """
        return await self.connection_pool.close()

    async def connect(self) -> Connection:
        """
        Establishes a connection to the database and returns it.
        """
        return await asyncpg.connect(**self.credentials)
