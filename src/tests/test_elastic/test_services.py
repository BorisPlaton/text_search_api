import pytest

from elastic.services.deletes import delete_text_by_id
from elastic.services.selectors import get_similar_documents_ids


class TestDeleteServices:

    @pytest.mark.asyncio
    async def test_delete_text_by_id_returns_false_if_none_was_deleted(self, es):
        deleted_record_quantity = await delete_text_by_id(es, 1)
        assert not deleted_record_quantity

    @pytest.mark.asyncio
    async def test_delete_text_by_id_returns_true_if_record_was_deleted(self, es, add_doc_to_index):
        res = await add_doc_to_index()
        doc_id = res.iD
        deleted_record_quantity = await delete_text_by_id(es, doc_id)
        assert deleted_record_quantity
        res = await es.search(index='documents', query={'term': {'iD': doc_id}})
        assert not res['hits']['hits']


class TestSelectServices:

    @pytest.mark.asyncio
    async def test_get_similar_documents_ids_returns_empty_list_if_none_was_found(self, es):
        res = await get_similar_documents_ids(es, 'string')
        assert isinstance(res, list)
        assert not res

    @pytest.mark.asyncio
    async def test_get_similar_documents_ids_returns_list_with_iD_fields(self, es, add_doc_to_index):
        doc = await add_doc_to_index()
        res = await get_similar_documents_ids(es, doc.text)
        assert len(res) == 1
        assert res[0] == doc.iD
