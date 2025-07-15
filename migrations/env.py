from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base  # Import your Base
import app.models.base  # Ensures TimestampedModel is loaded
import app.models.trip
import app.models.expense
import app.models.app_config
from app.config import load_config
import logging

config = context.config
logging.basicConfig(level=logging.INFO)  # Force INFO output, overrides fileConfig issues
logging.getLogger('alembic').setLevel(logging.DEBUG)  # Specific DEBUG for Alembic
# fileConfig(config.config_file_name)
target_metadata = Base.metadata
print("Alembic env loaded, DB URL:", load_config().DATABASE_URL)
from alembic.migration import MigrationContext

connection = context.get_bind()  # Get connection
migration_ctx = MigrationContext.configure(connection)
current_rev = migration_ctx.get_current_revision()
print("Current revision:", current_rev or "None (base)")

def run_migrations_offline():
    url = load_config().DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

def run_migrations_online():
    db_url = load_config().DATABASE_URL
    config.set_main_option('sqlalchemy.url', db_url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()