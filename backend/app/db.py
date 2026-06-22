"""Conexión a la base de datos y utilidades de sesión."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session

from app.settings import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine() -> Engine:
    """Engine perezoso: se crea (e importa el driver) al usarse, no al importar el módulo."""
    return create_engine(get_settings().database_url, future=True)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Sesión transaccional: commit al salir, rollback si hay excepción."""
    session = Session(bind=get_engine(), expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Iterator[Session]:
    """Dependencia FastAPI: sesión de solo lectura por petición."""
    session = Session(bind=get_engine(), expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Crea extensiones (vector, pg_trgm, unaccent), tablas e índices. Idempotente."""
    import app.models  # noqa: F401  -- registra los modelos en Base.metadata

    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS unaccent"))
    Base.metadata.create_all(engine)
    with engine.begin() as connection:
        # Índice trigram para la parte léxica de la búsqueda híbrida.
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_rag_chunks_texto_trgm "
                "ON rag_chunks USING gin (texto gin_trgm_ops)"
            )
        )
        # Índice HNSW para la búsqueda vectorial (coseno). Sin él, pgvector hace un
        # escaneo secuencial completo: aceptable con pocos chunks, lento al escalar.
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_rag_chunks_embedding_hnsw "
                "ON rag_chunks USING hnsw (embedding vector_cosine_ops)"
            )
        )
