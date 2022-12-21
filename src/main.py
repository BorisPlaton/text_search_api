from typing import Callable

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from config.settings import settings
from database.db import Database
from text_searcher.views import router as text_searcher_router


DESCRIPTION = """
The application for searching documents via text fragments. It is a solution for the
test [task](https://freezing-helicopter-7fb.notion.site/Python-67777c95bdbe4e59856c59b707349f2d).
"""


def create_app():
    """
    The factory function. Returns a FastAPI application instance.
    """
    db = Database()
    app = FastAPI(
        title="Text Searcher",
        description=DESCRIPTION,
        openapi_tags=[
            {
                "name": "Text documents",
                "description": "You can receive or delete them.",
            },
        ]
    )
    app.include_router(text_searcher_router)

    @app.middleware("http")
    async def set_db_connection(request: Request, call_next: Callable):
        """
        Gets a db connection from the connection pool and sets it to
        the request, so the service layer can use it.
        """
        async with db.connection_pool.acquire() as con:
            request.state.connection = con
            return await call_next(request)

    @app.on_event('startup')
    async def initialize_connection_pool():
        """
        Initialize a connection pool.
        """
        return await db.create_connection_pool()

    @app.on_event('shutdown')
    async def shutdown_connection_pool():
        """
        Close all connections in the pool.
        """
        return await db.close_connection_pool()

    return app


if __name__ == '__main__':
    uvicorn.run(
        "main:create_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        factory=True
    )
