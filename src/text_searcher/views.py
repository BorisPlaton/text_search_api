from asyncpg import Connection
from fastapi import APIRouter, Depends

from database.dependencies import get_db_connection
from text_searcher.schemas import TextFragment


router = APIRouter(
    prefix='/text',
    tags=['Text documents'],
)


@router.post(
    '/',
    description="Returns the list of text documents whose content matches the given one."
)
async def get_text_documents(text: TextFragment, db: Connection = Depends(get_db_connection)):
    pass


@router.delete(
    '/{document_id}',
    description="Deletes a specific text document whose id matches the given one."
)
async def delete_text_document(document_id: int):
    pass
