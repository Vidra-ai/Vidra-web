"""Cliente LLM desacoplado del proveedor.

Gemini (vía REST) u OpenAI (Chat Completions). Todo depende del protocolo `LLMClient`.
"""

from __future__ import annotations

from typing import Any, Protocol

import httpx

from app.settings import Settings

_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_OPENAI_URL = "https://api.openai.com/v1/chat/completions"


class LLMClient(Protocol):
    def generate(self, system: str, user: str) -> str: ...

    def generate_text(self, system: str, user: str) -> str: ...

    def generate_grounded(self, system: str, user: str) -> str: ...

    def generate_with_history(self, system: str, messages: list[dict[str, str]]) -> str: ...


class GeminiClient:
    """Cliente de Gemini sobre la API REST de Generative Language."""

    def __init__(self, api_key: str, model: str, *, timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        if not self._api_key:
            raise ValueError("GEMINI_API_KEY no puede estar vacía.")

    def _post(self, payload: dict[str, Any]) -> str:
        response = httpx.post(
            _GEMINI_URL.format(model=self._model),
            params={"key": self._api_key},
            json=payload,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return _first_text(response.json())

    def generate(self, system: str, user: str) -> str:
        return self._post(
            {
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
            }
        )

    def generate_text(self, system: str, user: str) -> str:
        return self._post(
            {
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
            }
        )

    def generate_grounded(self, system: str, user: str) -> str:
        return self._post(
            {
                "systemInstruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
                "tools": [{"google_search": {}}],
            }
        )

    def generate_with_history(self, system: str, messages: list[dict[str, str]]) -> str:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return self.generate_text(system, last_user)


def _first_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates")
    if not candidates:
        raise ValueError("Respuesta de Gemini sin 'candidates'")
    parts = candidates[0]["content"]["parts"]
    return "".join(part.get("text", "") for part in parts)


class FakeLLMClient:
    """Cliente de pruebas: devuelve una respuesta fija, sin red."""

    def __init__(self, response: str) -> None:
        self._response = response

    def generate(self, system: str, user: str) -> str:
        return self._response

    def generate_text(self, system: str, user: str) -> str:
        return self._response

    def generate_grounded(self, system: str, user: str) -> str:
        return self._response

    def generate_with_history(self, system: str, messages: list[dict[str, str]]) -> str:
        return self._response


class OpenAIClient:
    """Cliente de OpenAI sobre la API de Chat Completions."""

    def __init__(self, api_key: str, model: str, *, timeout: float = 30.0) -> None:
        self._api_key = api_key
        self._model = model
        self._timeout = timeout
        if not self._api_key:
            raise ValueError("OPENAI_API_KEY no puede estar vacía.")

    def _post(self, system: str, user: str) -> str:
        response = httpx.post(
            _OPENAI_URL,
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": self._model,
                "temperature": 1.2,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def generate(self, system: str, user: str) -> str:
        return self._post(system, user)

    def generate_text(self, system: str, user: str) -> str:
        return self._post(system, user)

    def generate_grounded(self, system: str, user: str) -> str:
        return self._post(system, user)

    def generate_with_history(self, system: str, messages: list[dict[str, str]]) -> str:
        response = httpx.post(
            _OPENAI_URL,
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={"model": self._model, "temperature": 1.2, "messages": [{"role": "system", "content": system}, *messages]},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def get_llm_client(settings: Settings) -> LLMClient:
    """Devuelve el cliente LLM según el proveedor configurado."""
    if settings.llm_provider == "gemini":
        return GeminiClient(settings.gemini_api_key, settings.llm_model)
    if settings.llm_provider == "openai":
        return OpenAIClient(settings.openai_api_key, settings.llm_model)
    raise ValueError(f"Proveedor LLM no soportado: {settings.llm_provider}")
