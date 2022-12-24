#!/usr/bin/env python
import asyncio

from database.db import Database
from database.services.documents.selectors import get_all_documents
from elastic.client import ElasticsearchClient


async def load_document_texts_to_index():
    """
    Loads document texts to the Elasticsearch index. Only documents
    which ids not already in the index are loaded.
    """
    client = ElasticsearchClient()
    documents = await get_all_documents(await Database().connect())
    await client.es.bulk(
        operations=[
            {
                'text': row['text'],
                'iD': row['id'],
            }
            for row in documents
        ],
    )


if __name__ == '__main__':
    asyncio.run(load_document_texts_to_index())
