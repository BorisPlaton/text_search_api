#!/usr/bin/env python
import asyncio

from elasticsearch import ApiError

from elastic.client import ElasticsearchClient


async def create_elastic_indices():
    """
    Creates specified indices in the Elasticsearch client.
    """
    client = ElasticsearchClient()
    try:
        await client.create_indices()
    except ApiError as e:
        print(str(e))
    else:
        print("All indices are created.")
    finally:
        await client.es.close()


if __name__ == '__main__':
    asyncio.run(create_elastic_indices())
