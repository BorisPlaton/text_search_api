from elasticsearch import AsyncElasticsearch


async def delete_text_by_id(es: AsyncElasticsearch, document_id: int):
    """
    Deletes document from the index by its iD field.
    """
    return await es.delete_by_query(
        index='documents', query={'term': {'iD': document_id}}
    )
