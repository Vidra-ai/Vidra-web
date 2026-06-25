"""Traducción automática de artículos ES → EN con Claude Haiku.

Paso final del pipeline: genera una variante inglesa del artículo para el blog.
Usa RESEARCH_MODEL (Haiku) — la traducción no requiere el escritor principal.
"""

from __future__ import annotations

from slugify import slugify

from app.content.generation.llm import LLMClient, RESEARCH_MODEL
from app.content.models import Article
from app.content.utils.logging import get_logger

log = get_logger()

_SYSTEM = (
    "You are a professional translator for a technical AI consulting blog. "
    "Translate Spanish content to clear, professional British/American English. "
    "Preserve ALL markdown formatting exactly: ## headings, **bold**, tables, "
    "--- separators, bullet lists, numbered lists, inline code, links."
)


def translate_to_english(article: Article, llm: LLMClient) -> dict | None:
    """Traduce title, meta y body de un artículo al inglés con Haiku.

    Devuelve un dict con keys: title, meta_description, slug, body_markdown.
    Devuelve None si la API falla o la respuesta es incompleta.
    """
    prompt = (
        "Translate the following Spanish blog article to English.\n\n"
        "Return EXACTLY this format — no preamble, no commentary:\n"
        "EN_TITLE: <translated title>\n"
        "EN_META: <translated meta description, max 155 chars>\n"
        "EN_SLUG: <English URL slug: lowercase, hyphens, no accents>\n"
        "EN_BODY:\n"
        "<translated markdown body — keep ALL markdown intact>\n\n"
        "--- ARTICLE ---\n"
        f"TITLE: {article.title}\n"
        f"META: {article.meta_description}\n"
        f"BODY:\n{article.body_markdown}"
    )

    try:
        raw = llm.complete(_SYSTEM, prompt, max_tokens=8192, model=RESEARCH_MODEL)
    except Exception as exc:
        log.error("[translator] Error al llamar a Haiku: %s", exc)
        return None

    result = _parse(raw)
    if result:
        log.info("[translator] Traducción OK — EN slug: %s (%d chars)", result["slug"], len(result["body_markdown"]))
    return result


def _parse(raw: str) -> dict | None:
    """Parsea la respuesta estructurada de Haiku."""
    fields: dict[str, str] = {"EN_TITLE": "", "EN_META": "", "EN_SLUG": ""}
    current: str | None = None
    body_lines: list[str] = []

    for line in raw.splitlines():
        key = line.split(":", 1)[0].strip().upper() if ":" in line else ""
        if key in fields:
            fields[key] = line.split(":", 1)[1].strip()
            current = key
        elif key == "EN_BODY":
            current = "EN_BODY"
        elif current == "EN_BODY":
            body_lines.append(line)

    title = fields["EN_TITLE"]
    meta = fields["EN_META"][:155]
    body = "\n".join(body_lines).strip()

    if not title or not body:
        log.error("[translator] Respuesta incompleta: title=%r body_len=%d", title, len(body))
        return None

    slug = slugify(fields["EN_SLUG"] or title)
    return {"title": title, "meta_description": meta, "slug": slug, "body_markdown": body}
