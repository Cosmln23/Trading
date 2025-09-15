from alembic import context
from sqlalchemy import engine_from_config, pool
import os

config = context.config

def get_url():
    url = os.getenv('DATABASE_URL', '')
    if not url:
        # Fallback to alembic.ini sqlalchemy.url
        return config.get_main_option("sqlalchemy.url")
    return url

def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=None, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        url=get_url(),
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
