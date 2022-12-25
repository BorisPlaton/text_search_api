from starlette.requests import Request


def get_db_connection(request: Request):
    """
    Returns a database connection that is stored in the request
    context.
    """
    return request.state.conn
