"""Generación de embeddings vía la API de OpenAI."""

from __future__ import annotations

import httpx

from app.settings import get_settings

_BATCH_SIZE = 32
_OPENAI_EMBED_URL = "https://api.openai.com/v1/embeddings"


def embed(texts: list[str]) -> list[list[float]]:
    """Devuelve embeddings para una lista de textos. Envía en lotes de _BATCH_SIZE."""
    settings = get_settings()
    results: list[list[float]] = []
    for i in range(0, len(texts), _BATCH_SIZE):
        batch = texts[i : i + _BATCH_SIZE]
        response = httpx.post(
            _OPENAI_EMBED_URL,
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={"model": settings.embedding_model, "input": batch},
            timeout=60.0,
        )
        response.raise_for_status()
        data = response.json()["data"]
        results.extend(item["embedding"] for item in data)
    return results


def embed_one(text: str) -> list[float]:
    return embed([text])[0]
