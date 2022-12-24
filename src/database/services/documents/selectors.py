from asyncpg import Connection, Record


async def get_all_documents(conn: Connection) -> list[Record]:
    """
    Returns all documents.
    """
    return await conn.fetch("SELECT * FROM document")
