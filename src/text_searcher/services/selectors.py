from asyncpg import Connection
from elasticsearch import AsyncElasticsearch

from database.services.documents.selectors import get_documents_by_ids
from elastic.services.selectors import get_similar_documents_ids
from text_searcher.schemas import Document


async def get_similar_documents_from_db(
        conn: Connection, es: AsyncElasticsearch, text: str, quantity: int = 20
) -> list[Document | None]:
    """
    Returns documents from the database which text content
    is similar to the given one.
    """
    documents_ids = await get_similar_documents_ids(es, text, quantity)
    if not documents_ids:
        return []
    documents = await get_documents_by_ids(conn, documents_ids)
    return [Document(**document) for document in documents]
