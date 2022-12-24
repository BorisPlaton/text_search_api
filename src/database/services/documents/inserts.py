from datetime import datetime

from asyncpg import Connection


async def insert_new_document(conn: Connection, rubrics: list[str], text: str, created_date: datetime):
    """
    Inserts a new document and returns the db response.
    """
    return await conn.execute(
        """
        INSERT INTO document(rubrics, text, created_date)
        VALUES
            ($1, $2, $3);
        """, rubrics, text, created_date
    )
