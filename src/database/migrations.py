from yoyo import get_backend, read_migrations

from config.settings import settings


class DBMigrations:
    """
    Handles database migrations.
    """

    def __init__(self):
        self.migrations_path = settings.BASE_DIR / 'database' / 'migrations'
        self.db_uri = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@" \
                      f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

    def migrate(self):
        """
        Applies migrations to the database.
        """
        backend = get_backend(self.db_uri)
        with backend.lock():
            backend.apply_migrations(
                backend.to_apply(read_migrations(str(self.migrations_path)))
            )
