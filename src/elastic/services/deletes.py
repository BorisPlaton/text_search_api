from elasticsearch import AsyncElasticsearch


async def delete_text_by_id(es: AsyncElasticsearch, document_id: int) -> bool:
    """
    Deletes document from the index by its iD field. Returns True
    or False depending on if document was deleted.
    """
    deleted_records = await es.delete_by_query(
        index='documents', query={'term': {'iD': document_id}},
        refresh=True
    )
    return bool(deleted_records['deleted'])
