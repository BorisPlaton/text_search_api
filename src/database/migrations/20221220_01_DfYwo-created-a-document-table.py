"""
Creates a Document table.
"""

from yoyo import step


__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE document (
            id int GENERATED ALWAYS AS IDENTITY NOT NULL,
            rubrics text[] NOT NULL,
            text text NOT NULL,
            created_date timestamp NOT NULL 
        );
        """,
        """
        DROP TABLE document;
        """,
    )
]
