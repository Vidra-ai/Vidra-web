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


@lru_cache
def get_settings() -> Settings:
    return Settings()
