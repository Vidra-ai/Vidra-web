"""Descubrimiento de temas mediante búsqueda web activa con Claude Haiku.

Se usa como fallback cuando RSS no devuelve resultados suficientes.
Haiku ejecuta las queries del tenant con la herramienta web_search y extrae
los temas más relevantes en formato estructurado.
"""

from __future__ import annotations

import json

from app.content.config import env
from app.content.generation.llm import RESEARCH_MODEL
from app.content.models import Topic, TopicOrigin
from app.content.sources.base import BaseSource
from app.content.utils.logging import get_logger

log = get_logger()

_EXTRACT_SYSTEM = (
    "Eres un asistente de investigación de contenido. "
    "Responde siempre en español. "
    "Tu tarea es identificar noticias o artículos relevantes para el sector indicado "
    "y devolverlos en JSON estricto, sin texto adicional."
)

_EXTRACT_PROMPT = """\
Sector: {sector}
Búsqueda realizada: "{query}"

A partir de los resultados de búsqueda que tienes disponibles, extrae hasta {limit} \
noticias o artículos relevantes para este sector.

Devuelve ÚNICAMENTE un array JSON con esta estructura (sin markdown, sin explicaciones):
[
  {{
    "title": "Título de la noticia",
    "summary": "Resumen de 2-3 frases sobre el contenido",
    "url": "URL del artículo si está disponible, o null"
  }}
]
"""


class WebSearchSource(BaseSource):
    """Usa el web search tool de Claude Haiku para buscar noticias del sector."""

    name = "web_search"

    def discover(self, limit: int = 5) -> list[Topic]:
        queries = self.tenant.sources.web_search_queries
        if not queries:
            log.info("Tenant '%s': no hay queries de web_search configuradas.", self.tenant.slug)
            return []

        api_key = env("CONTENT_ANTHROPIC_API_KEY")
        if not api_key:
            log.warning("CONTENT_ANTHROPIC_API_KEY no configurada: web_search_source no disponible.")
            return []

        try:
            import anthropic
        except ImportError:
            log.warning("SDK 'anthropic' no instalado: web_search_source no disponible.")
            return []

        client = anthropic.Anthropic(api_key=api_key)
        topics: list[Topic] = []
        per_query = max(1, limit // len(queries))

        for query in queries:
            if len(topics) >= limit:
                break
            new = self._search_query(client, query, per_query)
            topics.extend(new)
            log.info("Web search '%s' → %d temas encontrados", query, len(new))

        return topics[:limit]

    def _search_query(self, client, query: str, limit: int) -> list[Topic]:
        """Ejecuta una query y extrae Topics del resultado."""
        try:
            resp = client.messages.create(
                model=RESEARCH_MODEL,
                max_tokens=1024,
                tools=[{"type": "web_search_20260209", "name": "web_search"}],
                # tool_choice auto: Haiku decide si usar la herramienta
                system=_EXTRACT_SYSTEM,
                messages=[
                    {
                        "role": "user",
                        "content": _EXTRACT_PROMPT.format(
                            sector=self.tenant.brand.sector,
                            query=query,
                            limit=limit,
                        ),
                    }
                ],
            )
        except Exception as exc:
            log.warning("Error en web_search para query '%s': %s", query, exc)
            return []

        raw_text = "".join(
            block.text for block in resp.content if hasattr(block, "text")
        )
        return _parse_topics(raw_text, query)


def _parse_topics(raw: str, query: str) -> list[Topic]:
    """Parsea el JSON devuelto por Haiku y construye Topics."""
    raw = raw.strip()
    # Haiku a veces envuelve el JSON en ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        items = json.loads(raw)
        if not isinstance(items, list):
            return []
    except json.JSONDecodeError:
        log.warning("WebSearchSource: respuesta no es JSON válido.")
        return []

    topics = []
    for item in items:
        if not isinstance(item, dict) or not item.get("title"):
            continue
        topics.append(
            Topic(
                title=item["title"],
                summary=item.get("summary", ""),
                origin=TopicOrigin.NEWS,
                source_url=item.get("url"),
                source_name=f"web_search:{query}",
                raw=item.get("summary", ""),
            )
        )
    return topics
