from datetime import datetime

from pydantic import BaseModel


class TextFragment(BaseModel):
    """
    Receives a text fragment which is used for searching the documents.
    """
    text: str


class Document(BaseModel):
    """
    The document with text from the database.
    """
    id: int
    text: str
    rubrics: list[str]
    created_date: datetime
