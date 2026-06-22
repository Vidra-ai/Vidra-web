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

    # Orígenes permitidos para CORS (separados por comas). En producción debe ser
    # el dominio público de la web, nunca "*" cuando se usan credenciales.
    cors_origins: str = "http://localhost:4322,http://localhost:4321,https://vidra-ia.com"

    # Rate limiting del endpoint público /rag/chat (por IP, ventana deslizante).
    chat_rate_limit: int = 20
    chat_rate_window: int = 60

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
