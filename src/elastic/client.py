from elasticsearch import AsyncElasticsearch

from config.settings import settings
from elastic.indices import DocumentsIndex


class ElasticsearchClient:
    """
    The async Elasticsearch client.
    """

    def __init__(self):
        self.es = AsyncElasticsearch(
            f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"
        )
        self.indices = [
            DocumentsIndex()
        ]

    async def create_indices(self):
        """
        Creates all specified indices.
        """
        for index in self.indices:
            await index.create(self.es)
