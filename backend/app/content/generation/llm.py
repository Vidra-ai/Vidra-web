"""Capa aislada del proveedor LLM. Cambiar de proveedor = tocar solo este archivo.

Por defecto usa Claude (Anthropic). El modelo se toma de CONTENT_LLM_MODEL.

Dos roles definidos:
  - RESEARCH_MODEL: rápido y barato, para filtrar/resumir noticias (Haiku).
  - WRITING_MODEL:  máxima calidad, para redactar artículos SEO (Sonnet/Opus).
"""

from __future__ import annotations

from app.content.config import env
from app.content.utils.logging import get_logger

log = get_logger()

WRITING_MODEL = "claude-sonnet-4-6"
RESEARCH_MODEL = "claude-haiku-4-5"


class LLMClient:
    """Cliente de generación de texto con soporte de rol (research / writing)."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or env("CONTENT_LLM_MODEL", WRITING_MODEL)
        # Clave dedicada del motor de contenido (proyecto Anthropic propio, para aislar
        # el gasto del chatbot). Sin fallback a ANTHROPIC_API_KEY a propósito.
        self._api_key = env("CONTENT_ANTHROPIC_API_KEY")
        self._client = None  # inicialización perezosa

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def complete(
        self,
        system: str,
        prompt: str,
        max_tokens: int = 4096,
        model: str | None = None,
    ) -> str:
        """Genera texto.

        `model` sobreescribe el modelo del cliente para esta llamada concreta,
        lo que permite usar Haiku en pasos de investigación y Sonnet/Opus en
        redacción desde el mismo cliente o desde clientes de rol diferente.
        """
        if not self._api_key:
            log.warning("ANTHROPIC_API_KEY no configurada: devolviendo contenido placeholder.")
            return _placeholder(prompt)

        try:
            client = self._get_client()
        except ImportError:
            log.warning("SDK 'anthropic' no instalado: devolviendo placeholder.")
            return _placeholder(prompt)

        effective_model = model or self.model
        log.debug("LLM call → model=%s max_tokens=%d", effective_model, max_tokens)

        # adaptive thinking solo disponible en Opus 4.6+ y Sonnet 4.6+; no en Haiku.
        supports_thinking = "haiku" not in effective_model
        kwargs = {"thinking": {"type": "adaptive"}} if supports_thinking else {}

        # Streaming obligatorio para max_tokens altos (evita timeout de 10 min del SDK).
        # get_final_message() es más robusto que get_final_text() cuando hay thinking blocks.
        with client.messages.stream(
            model=effective_model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        ) as stream:
            final = stream.get_final_message()
            return "".join(block.text for block in final.content if block.type == "text")


def _placeholder(prompt: str) -> str:
    return (
        "[CONTENIDO PLACEHOLDER — configura ANTHROPIC_API_KEY para generación real]\n\n"
        f"Prompt recibido (recorte):\n{prompt[:400]}"
    )
