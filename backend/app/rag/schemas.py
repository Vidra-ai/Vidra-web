from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class MensajeHistorial(BaseModel):
    rol: Literal["usuario", "asistente"]
    contenido: str = Field(..., min_length=1, max_length=2000)


class DocumentMeta(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    titulo: str
    tipo: str | None = None
    area: str | None = None
    fuente_original: str | None = None
    nivel_confidencialidad: str
    created_at: datetime


class ChatSource(BaseModel):
    doc_id: int
    titulo: str
    seccion: str | None = None
    chunk_texto: str
    similaridad: float


class ChatRequest(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(10, ge=1, le=20)
    historial: list[MensajeHistorial] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    respuesta: str
    fuentes: list[ChatSource]
    sin_informacion: bool


class ChatSourcePublic(BaseModel):
    """Versión pública de ChatSource — omite campos internos (doc_id, chunk_texto, similaridad)."""
    titulo: str
    seccion: str | None = None


class ChatResponsePublic(BaseModel):
    """Schema de respuesta del endpoint público /rag/chat."""
    respuesta: str
    fuentes: list[ChatSourcePublic]
    sin_informacion: bool


class RagSourceIn(BaseModel):
    url: HttpUrl
    titulo: str
    tipo: str | None = None
    area: str | None = None


class RagSourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    titulo: str
    tipo: str | None
    area: str | None
    content_hash: str | None
    doc_id: int | None
    last_synced_at: datetime | None
    enabled: bool
    created_at: datetime


class SyncResultItem(BaseModel):
    source_id: int
    url: str
    status: str  # "updated" | "unchanged" | "error"
    detail: str | None = None


class SyncResult(BaseModel):
    synced: int
    unchanged: int
    errors: int
    items: list[SyncResultItem]
