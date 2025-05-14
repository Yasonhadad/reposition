from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# מייבאים את המודלים כדי להירשם אוטומטית ל־SQLModel.metadata
from app import models  # noqa: F401

# Alembic Config object
config = context.config

# מחליפים את asyncpg ב-psycopg2 כדי שהמיגרציות ירוצו עם DBAPI סינכרוני
from app.db import DATABASE_URL
sync_url = DATABASE_URL.replace("asyncpg", "psycopg2")
config.set_main_option("sqlalchemy.url", sync_url)

# Load logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata של כל המודלים
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """מיגרציה במצב offline — כותב SQL בלבד."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """מיגרציה במצב online — מתחבר למסד ומריץ."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

# בוחרים מצב הפעלה
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
