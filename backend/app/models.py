from __future__ import annotations

from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.settings import get_settings

_EMBEDDING_DIM = get_settings().embedding_dim


class RagDocument(Base):
    __tablename__ = "rag_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    tipo: Mapped[str | None] = mapped_column(default=None)
    area: Mapped[str | None] = mapped_column(default=None)
    fuente_original: Mapped[str | None] = mapped_column(default=None)
    # Hash SHA-256 del contenido fuente. Permite re-embeber solo los ficheros
    # que cambian en la sincronización incremental (p. ej. notas de Obsidian).
    content_hash: Mapped[str | None] = mapped_column(default=None)
    nivel_confidencialidad: Mapped[str] = mapped_column(default="interno")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RagSource(Base):
    __tablename__ = "rag_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    titulo: Mapped[str]
    tipo: Mapped[str | None] = mapped_column(default=None)
    area: Mapped[str | None] = mapped_column(default=None)
    content_hash: Mapped[str | None] = mapped_column(default=None)
    doc_id: Mapped[int | None] = mapped_column(
        ForeignKey("rag_documents.id", ondelete="SET NULL"), default=None
    )
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RagChunk(Base):
    __tablename__ = "rag_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(
        ForeignKey("rag_documents.id", ondelete="CASCADE"), index=True
    )
    texto: Mapped[str]
    pagina: Mapped[int | None] = mapped_column(default=None)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(_EMBEDDING_DIM), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
