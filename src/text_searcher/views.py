from asyncpg import Connection
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends

from database.dependencies import get_db_connection
from elastic.dependecies import get_elastic_client
from text_searcher.schemas import TextFragment, Document
from text_searcher.services.deletes import delete_completely_document_by_id
from text_searcher.services.selectors import get_similar_documents_from_db


router = APIRouter(
    prefix='/text',
    tags=['Text documents'],
)


@router.post(
    '/',
    description="Returns the list of text documents whose content matches the given one."
)
async def get_text_documents(
        text: TextFragment, conn: Connection = Depends(get_db_connection),
        es: AsyncElasticsearch = Depends(get_elastic_client)
) -> list[Document | None]:
    return await get_similar_documents_from_db(conn, es, text.text)


@router.delete(
    '/{document_id}',
    description="Deletes a specific text document whose id matches the given one."
)
async def delete_text_document(
        document_id: int, conn: Connection = Depends(get_db_connection),
        es: AsyncElasticsearch = Depends(get_elastic_client)
) -> Document | None:
    return await delete_completely_document_by_id(conn, es, document_id)
