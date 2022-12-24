#!/usr/bin/env python
import asyncio

from elasticsearch import Elasticsearch, ApiError
from elasticsearch.helpers import bulk

from database.db import Database
from database.services.documents.selectors import get_all_documents
from elastic.client import ElasticsearchClient


async def load_document_texts_to_index_from_db():
    """
    Loads document texts to the Elasticsearch index. Only documents
    which ids not already in the index are loaded.
    """
    es = Elasticsearch(ElasticsearchClient().elastic_uri)
    documents = await get_all_documents(await Database().connect())
    try:
        res = bulk(es, [{'_index': 'documents', 'text': row['text'], 'iD': row['id']} for row in documents])
    except ApiError as e:
        print(str(e))
    else:
        print(f"{res[0]} documents have been inserted.")
    finally:
        es.close()


if __name__ == '__main__':
    asyncio.run(load_document_texts_to_index_from_db())
