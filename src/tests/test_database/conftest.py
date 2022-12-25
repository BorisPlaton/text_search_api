import pytest


@pytest.fixture
def add_document():
    def inner():
        pass

    return inner
