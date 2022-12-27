from datetime import datetime

from pydantic import BaseModel


class TextFragment(BaseModel):
    """
    Receives a text fragment which is used for searching the documents.
    """
    text: str

    class Config:
        schema_extra = {
            'example': {
                'secret': "Text",
            }
        }


class Document(BaseModel):
    """
    The document with text from the database.
    """
    id: int
    text: str
    rubrics: list[str]
    created_date: datetime

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'text': "Matched text",
                'rubrics': ['rubric-1', 'rubric-2'],
                'created_date': '2019-11-12T21:10:52'
            }
        }
