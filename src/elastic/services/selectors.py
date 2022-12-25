from elasticsearch import AsyncElasticsearch


async def get_similar_documents_ids(
        es: AsyncElasticsearch, text_example: str, quantity: int = 10
) -> list[int | None]:
    """
    Returns records' ID field which text is similar to the given one.
    """
    res = await es.search(
        index='documents', size=quantity, source=['iD'],
        query={
            "match": {
                "text": text_example
            }
        }
    )
    return [hit['_source']['iD'] for hit in res.body['hits']['hits']]
