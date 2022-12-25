from unittest.mock import patch, MagicMock

import pytest

from text_searcher.schemas import Document
from text_searcher.services.deletes import delete_completely_document_by_id
from text_searcher.services.selectors import get_similar_documents_from_db


class TestSelectServices:

    @pytest.mark.asyncio
    async def test_get_similar_documents_from_db_returns_empty_list_if_none_were_found(self, conn, es):
        res = await get_similar_documents_from_db(conn, es, 'string')
        assert isinstance(res, list)
        assert not res

    @pytest.mark.asyncio
    async def test_get_similar_documents_from_db_returns_list_with_document_instances(
            self, conn, es, add_document, add_doc_to_index
    ):
        doc = await add_document()
        doc_text = doc['text']
        await add_doc_to_index(doc['id'], doc_text)
        res = await get_similar_documents_from_db(conn, es, doc_text)
        assert isinstance(res, list)
        assert len(res) == 1
        for field, value in doc.items():
            assert getattr(res[0], field) == value


class TestDeleteServices:

    @pytest.mark.asyncio
    async def test_delete_completely_document_by_id_deletes_from_index_and_db(
            self, conn, es, add_document, add_doc_to_index
    ):
        doc = await add_document()
        doc_id = doc['id']
        doc_text = doc['text']
        await add_doc_to_index(doc_id, doc_text)
        deleted_doc = await delete_completely_document_by_id(conn, es, doc_id)
        assert isinstance(deleted_doc, Document)
        for field, value in doc.items():
            assert getattr(deleted_doc, field) == value
        db_response = await conn.fetchrow("SELECT * FROM document WHERE id = $1;", doc_id)
        es_response = await es.search(index='documents', query={'term': {'iD': doc_id}})
        assert db_response is None
        assert not es_response['hits']['hits']

    @pytest.mark.asyncio
    @patch('text_searcher.services.deletes.delete_text_by_id')
    async def test_delete_completely_document_rollbacks_if_elastic_fails(
            self, mocked_func: MagicMock, conn, es, add_document, add_doc_to_index
    ):
        def raise_exc(*args):
            raise ValueError

        mocked_func.side_effect = raise_exc
        doc = await add_document()
        doc_id = doc['id']
        doc_text = doc['text']
        await add_doc_to_index(doc_id, doc_text)
        try:
            await delete_completely_document_by_id(conn, es, doc_id)
        except ValueError:
            pass
        db_response = await conn.fetchrow("SELECT * FROM document WHERE id = $1;", doc_id)
        es_response = await es.search(index='documents', query={'term': {'iD': doc_id}})
        assert db_response == doc
        assert es_response['hits']['hits'][0]['_source']['iD'] == doc['id']
