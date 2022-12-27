from asyncpg import Connection
from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter, Depends
from fastapi.params import Path

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
    response_model=list[Document | None],
)
async def get_text_documents(
        text: TextFragment, conn: Connection = Depends(get_db_connection),
        es: AsyncElasticsearch = Depends(get_elastic_client)
):
    """
    Returns the list of text documents whose content matches the given one.
    If none, it returns an empty list.
    """
    return await get_similar_documents_from_db(conn, es, text.text)


@router.delete(
    '/{document_id}',
    response_model=Document,
    responses={
        404: {
            'description': "Document with given `ID` doesn't exist.",
            'content': {
                'application/json': {
                    'example': {
                        'detail': "Document with ID 2 doesn't exists"
                    }
                }
            }
        }
    }
)
async def delete_text_document(
        document_id: int = Path(..., title="Document ID", ge=1),
        conn: Connection = Depends(get_db_connection),
        es: AsyncElasticsearch = Depends(get_elastic_client)
):
    """
    Deletes a specific text document whose id matches the given one. If
    the document wasn't found, returns `Not found` response.
    """
    return await delete_completely_document_by_id(conn, es, document_id)
