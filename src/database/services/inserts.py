from datetime import datetime

from asyncpg import Connection, Record


async def insert_new_document(conn: Connection, rubrics: list[str], text: str, created_date: datetime) -> Record:
    """
    Inserts a new document and returns the newly created instances.
    """
    return await conn.fetchrow(
        """
        INSERT INTO document(rubrics, text, created_date)
        VALUES
            ($1, $2, $3)
        RETURNING *;
        """, rubrics, text, created_date
    )
