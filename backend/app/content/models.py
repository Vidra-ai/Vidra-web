"""Modelos de datos del dominio. Independientes del proveedor y del canal."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TopicOrigin(str, Enum):
    """De dónde nace un tema."""

    NEWS = "news"        # descubierto de fuentes de noticias (reactivo)
    MANUAL = "manual"    # aportado por la empresa: "lo que hemos hecho" (proactivo)


class Topic(BaseModel):
    """Tema candidato para generar contenido."""

    title: str
    summary: str = ""
    origin: TopicOrigin = TopicOrigin.NEWS
    source_url: str | None = None
    source_name: str | None = None
    published_at: datetime | None = None
    raw: str = ""  # texto de partida (noticia o nota manual)


class Article(BaseModel):
    """Artículo web optimizado para SEO."""

    title: str                       # H1 / título visible
    seo_title: str                   # <title>, <= 60 car.
    meta_description: str             # <= 155 car.
    slug: str
    body_markdown: str
    primary_keyword: str
    keywords: list[str] = Field(default_factory=list)
    topic: Topic | None = None


class SocialVariant(BaseModel):
    """Adaptación del mensaje a un canal social concreto."""

    channel: str                     # "linkedin", "x", "instagram"...
    text: str
    hashtags: list[str] = Field(default_factory=list)
    link: str | None = None
    media_paths: list[str] = Field(default_factory=list)


class PublishResult(BaseModel):
    """Resultado de publicar en un canal."""

    channel: str
    success: bool
    dry_run: bool = False
    url: str | None = None
    external_id: str | None = None
    message: str = ""
