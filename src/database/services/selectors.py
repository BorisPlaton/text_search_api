from asyncpg import Connection, Record


async def get_all_documents(conn: Connection) -> list[Record | None]:
    """
    Returns all documents.
    """
    return await conn.fetch("SELECT * FROM document;")


async def get_documents_by_ids(conn: Connection, ids: list[int]) -> list[Record]:
    """
    Returns documents whose ID field is presented in the given
    IDs list.
    """
    return await conn.fetch(
        """
        SELECT * FROM document
        WHERE id = ANY($1::integer[])
        ORDER BY created_date DESC;
        """, ids
    )
