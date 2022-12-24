from starlette.requests import Request


def get_elastic_client(request: Request):
    """
    Returns an async Elasticsearch client from the request.
    """
    return request.app.state.es
