"""Carga y validación de la configuración de un tenant + secretos de entorno."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from app.content import paths


class Brand(BaseModel):
    sector: str
    audience: str = ""
    value_proposition: str = ""
    tone: str = ""
    expertise: list[str] = Field(default_factory=list)


class Seo(BaseModel):
    primary_keywords: list[str] = Field(default_factory=list)
    secondary_keywords: list[str] = Field(default_factory=list)
    internal_links_base: str = ""
    min_words: int = 800
    max_words: int = 1500


class Sources(BaseModel):
    # Nivel 1: sites prioritarios del sector
    priority_feeds: list[str] = Field(default_factory=list)
    # Nivel 2: Google News u otros feeds genéricos (fallback)
    google_news_feeds: list[str] = Field(default_factory=list)
    # Compatibilidad: campo legacy usado antes de la separación de niveles
    rss: list[str] = Field(default_factory=list)
    keywords_filter: list[str] = Field(default_factory=list)
    # Nivel 3: búsqueda web activa con Claude Haiku como último recurso
    web_search_fallback: bool = False
    web_search_queries: list[str] = Field(default_factory=list)


class Schedule(BaseModel):
    publish_web_first: bool = True
    social_delay_minutes: int = 30
    cadence: str = ""


class TenantConfig(BaseModel):
    """Configuración completa de una empresa (tenant)."""

    slug: str
    name: str
    language: str = "es"
    locale: str = "es-ES"
    brand: Brand
    seo: Seo = Field(default_factory=Seo)
    sources: Sources = Field(default_factory=Sources)
    channels: dict = Field(default_factory=dict)
    schedule: Schedule = Field(default_factory=Schedule)

    def channel_enabled(self, channel: str) -> bool:
        return bool(self.channels.get(channel, {}).get("enabled", False))


def load_tenant(slug: str, tenants_dir: Path | str | None = None) -> TenantConfig:
    """Carga y valida el YAML de un tenant."""
    base = Path(tenants_dir) if tenants_dir is not None else paths.tenants_dir()
    path = base / f"{slug}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No existe el tenant '{slug}' en {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return TenantConfig.model_validate(data)


def env(name: str, default: str | None = None) -> str | None:
    """Lee un secreto/ajuste de entorno (los secretos nunca van en el YAML)."""
    return os.environ.get(name, default)
