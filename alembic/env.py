from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import app.models  # noqa: F401 (garante import de todos os modelos)

# Carrega settings e modelos
from app.core.config import settings
from app.models import SQLModel  # importa também __all__ com tabelas

# Config Alembic
config = context.config

# Sobrescreve URL com .env / Settings, se houver
if config.get_main_option("sqlalchemy.url") is None:
    config.set_main_option("sqlalchemy.url", settings.database_url)

# Loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata alvo
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Modo offline (gera SQL sem conectar)."""
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
    """Modo online (conecta e executa)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
