"""Configuración del servicio, leída del entorno (12-factor)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://chatbot:changeme@db:5432/chatbot"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    gemini_api_key: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536
    admin_api_key: str = ""
    vidra_api_url: str = "http://vidra_api_core:8000"
    vidra_api_key: str = ""

    # Orígenes permitidos para CORS (separados por comas). En producción debe ser
    # el dominio público de la web, nunca "*" cuando se usan credenciales.
    cors_origins: str = "http://localhost:4322,http://localhost:4321,https://vidra-ia.com"

    # Rate limiting del endpoint público /rag/chat (por IP, ventana deslizante).
    chat_rate_limit: int = 20       # máx requests por ventana (por minuto)
    chat_rate_window: int = 60      # tamaño de la ventana en segundos
    chat_daily_limit: int = 100     # máx requests por IP por día natural

    # Caché de respuestas para preguntas idénticas (evita pagar dos veces).
    chat_cache_ttl: int = 3600      # segundos que dura una entrada en caché (1h)

    # Carpeta de Obsidian "Información pública" montada en el contenedor (solo lectura).
    # Vacío = desactivado. La sincronización incremental re-embebe solo los .md que cambian.
    public_docs_dir: str = ""
    public_docs_sync_interval: int = 10
    # Si True, solo se indexan notas con frontmatter `visibilidad: publico` (ADR-005).
    public_docs_require_public_flag: bool = True

    # Documentación interactiva (/docs, /redoc, /openapi.json). Desactivada por defecto
    # en producción. Activar solo en entorno local (API_DOCS_ENABLED=true en .env).
    api_docs_enabled: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
