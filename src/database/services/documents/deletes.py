from asyncpg import Connection, Record


async def delete_document_by_id(conn: Connection, document_id: int) -> Record:
    """
    Delete document by id and returns its data.
    """
    res = await conn.fetchrow(
        """
        DELETE FROM document WHERE id = $1 RETURNING *;
        """, document_id
    )
    return res
