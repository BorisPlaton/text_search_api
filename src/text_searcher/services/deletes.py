from asyncpg import Connection
from elasticsearch import AsyncElasticsearch

from database.services.deletes import delete_document_by_id
from elastic.services.deletes import delete_text_by_id
from text_searcher.schemas import Document


async def delete_completely_document_by_id(
        conn: Connection, es: AsyncElasticsearch, document_id: int
) -> Document | None:
    """
    Deletes document from the database and the index by
    its id. If document with such id is deleted, returns its
    columns. Otherwise, returns None.
    """
    async with conn.transaction():
        deleted_record = await delete_document_by_id(conn, document_id)
        if not deleted_record:
            return
        await delete_text_by_id(es, document_id)
    return Document(**deleted_record)
