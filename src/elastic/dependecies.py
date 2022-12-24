from elasticsearch import AsyncElasticsearch
from starlette.requests import Request


def get_elastic_client(request: Request) -> AsyncElasticsearch:
    """
    Returns an async Elasticsearch client from the request.
    """
    return request.app.state.es
