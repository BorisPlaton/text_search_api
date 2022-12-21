from pydantic import BaseModel


class TextFragment(BaseModel):
    """
    Receives a text fragment which is used for searching the documents.
    """
    text: str
