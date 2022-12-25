import pytest

from database.services.deletes import delete_document_by_id
from database.services.selectors import get_all_documents


class TestDeleteServices:

    @pytest.mark.asyncio
    async def test_delete_document_with_wrong_id(self, conn):
        assert not await get_all_documents(conn)
        assert await delete_document_by_id(conn, 1) is None
