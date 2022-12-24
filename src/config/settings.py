import os
from pathlib import Path

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    BASE_DIR = Path(__file__).parent.parent
    HOST: str = os.getenv('HOST')
    PORT: int = os.getenv('PORT')
    DEBUG: bool = bool(os.getenv('DEBUG'))

    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ELASTICSEARCH_PORT: str
    ELASTICSEARCH_HOST: str

    class Config:
        env_file = map(lambda x: Path(__file__).parent.parent.parent / x, ['.env.dist', '.env'])
        env_file_encoding = 'utf-8'
        allow_mutation = False


settings = ProjectSettings()
