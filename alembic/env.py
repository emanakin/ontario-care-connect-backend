import sys
import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# Add the parent directory of 'alembic' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("Current sys.path:", sys.path)

# Now you can import your app modules
from app.database import Base
import app.models  # Ensure all models are imported

# Alembic Config object
config = context.config
print("Alembic is using the database URL:", config.get_main_option("sqlalchemy.url"))

# Metadata for autogenerate
target_metadata = Base.metadata

# Configure logging
if config.config_file_name:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

