import pytest


class TestElasticsearchClient:

    @pytest.mark.asyncio
    async def test_elastic_client_created(self, es_client):
        assert await es_client.es.ping()

    @pytest.mark.asyncio
    async def test_all_indices_are_created(self, es_client):
        await es_client.es.indices.delete(
            index=[index.name for index in es_client.indices],
        )
        response = await es_client.es.indices.get_alias(index="*")
        assert not list(filter(lambda x: not x.startswith('.'), response.body))
        await es_client.create_indices()
        response = await es_client.es.indices.get_alias(index="*")
        indices_name = list(filter(lambda x: not x.startswith('.'), response.body))
        for index in es_client.indices:
            assert index.name in indices_name
