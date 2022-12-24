from functools import cached_property

from elasticsearch import AsyncElasticsearch

from config.settings import settings
from elastic.indices import DocumentsIndex


class ElasticsearchClient:
    """
    The async Elasticsearch client.
    """

    def __init__(self):
        self.es = AsyncElasticsearch(self.elastic_uri)
        self.indices = [DocumentsIndex()]

    async def create_indices(self):
        """
        Creates all specified indices.
        """
        for index in self.indices:
            await index.create(self.es)

    @cached_property
    def elastic_uri(self) -> str:
        """
        Returns URI to the elastic client.
        """
        return f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"
