"""
Creates a Document table.
"""

from yoyo import step


__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE document (
            id SERIAL PRIMARY KEY,
            rubrics TEXT[] NOT NULL,
            text TEXT NOT NULL,
            created_date TIMESTAMP NOT NULL 
        );
        """,
        """
        DROP TABLE document;
        """
    )
]
