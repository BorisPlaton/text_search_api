from datetime import datetime

import pytest
from asyncpg import Record

from database.services.deletes import delete_document_by_id
from database.services.inserts import insert_new_document
from database.services.selectors import get_all_documents, get_documents_by_ids


class TestDeleteServices:

    @pytest.mark.asyncio
    async def test_delete_document_with_wrong_id(self, conn):
        assert not await get_all_documents(conn)
        assert await delete_document_by_id(conn, 1) is None

    @pytest.mark.asyncio
    async def test_delete_document_returns_its_columns_if_exists(self, conn, add_document):
        doc_data = (['rubric'], 'some_text', datetime.now())
        res = await add_document(doc_data)
        deleted_record = await delete_document_by_id(conn, res['id'])
        assert isinstance(deleted_record, Record)
        for data in doc_data:
            assert data in deleted_record.values()
        assert deleted_record['id'] == res['id']


class TestInsertServices:

    @pytest.mark.asyncio
    async def test_insert_new_document_returns_all_created_columns(self, conn):
        doc_data = (['rubric'], 'some_text', datetime.now())
        created_doc = await insert_new_document(conn, *doc_data)
        assert isinstance(created_doc, Record)
        for data in doc_data:
            assert data in created_doc.values()
        assert created_doc['id']


class TestSelectServices:

    @pytest.mark.asyncio
    async def test_if_no_records_get_all_documents_returns_empty_list(self, conn):
        records_list = await get_all_documents(conn)
        assert isinstance(records_list, list)
        assert not records_list

    @pytest.mark.asyncio
    async def test_get_all_documents_returns_list_with_records(self, conn, add_document):
        doc_data = (['rubric'], 'some_text', datetime.now())
        res = await add_document(doc_data)
        records_list = await get_all_documents(conn)
        assert isinstance(records_list, list)
        assert len(records_list) == 1
        assert records_list[0] == res

    @pytest.mark.asyncio
    async def test_get_documents_by_ids_returns_empty_list_if_none_exists(self, conn):
        res = await get_documents_by_ids(conn, [])
        assert isinstance(res, list)
        assert not res

    @pytest.mark.asyncio
    async def test_get_documents_by_ids_returns_empty_list_if_invalid_id_given(self, conn):
        res = await get_documents_by_ids(conn, [1, -1])
        assert isinstance(res, list)
        assert not res

    @pytest.mark.asyncio
    async def test_get_documents_by_ids_returns_list_with_records(self, conn, add_document):
        doc = await add_document()
        tested_doc = await add_document()
        res = await get_documents_by_ids(conn, [tested_doc['id']])
        assert isinstance(res, list)
        assert len(res) == 1
        assert tested_doc != doc
        assert tested_doc == res[0]
