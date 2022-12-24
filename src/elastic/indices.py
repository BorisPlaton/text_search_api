from elasticsearch import AsyncElasticsearch


class DocumentsIndex:
    """
    The documents index.
    """

    def __init__(self):
        self.name = 'documents'
        self.mapping = {
            'properties': {
                'iD': {'type': 'integer', 'coerce': False},
                'text': {'type': 'text'}
            }
        }

    async def create(self, es: AsyncElasticsearch):
        """
        Creates a documents index.
        """
        return await es.indices.create(index=self.name, mappings=self.mapping)
