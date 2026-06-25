"""Reglas SEO: selección de keyword, slug, recortes de meta y parseo de la salida del LLM."""

from __future__ import annotations

from slugify import slugify

from app.content.config import TenantConfig
from app.content.models import Article, Topic

SEO_TITLE_MAX = 60
META_MAX = 155


def pick_primary_keyword(tenant: TenantConfig, topic: Topic) -> str:
    """Elige la keyword principal más afín al tema; si no, la primera del tenant."""
    blob = f"{topic.title} {topic.summary} {topic.raw}".lower()
    for kw in tenant.seo.primary_keywords:
        if any(word in blob for word in kw.lower().split()):
            return kw
    return tenant.seo.primary_keywords[0] if tenant.seo.primary_keywords else topic.title


def parse_article(raw: str, tenant: TenantConfig, topic: Topic, primary_keyword: str) -> Article:
    """Convierte la salida estructurada del LLM en un `Article`, aplicando límites SEO."""
    fields = {"TITULO": "", "SEO_TITLE": "", "META": "", "SLUG": "", "CUERPO": ""}
    current = None
    body_lines: list[str] = []
    for line in raw.splitlines():
        header = line.split(":", 1)[0].strip().upper() if ":" in line else ""
        if header in fields and header != "CUERPO":
            fields[header] = line.split(":", 1)[1].strip()
            current = header
        elif header == "CUERPO":
            current = "CUERPO"
        elif current == "CUERPO":
            body_lines.append(line)

    title = fields["TITULO"] or topic.title
    seo_title = (fields["SEO_TITLE"] or title)[:SEO_TITLE_MAX]
    meta = (fields["META"] or topic.summary)[:META_MAX]
    slug = slugify(fields["SLUG"] or title)
    body = "\n".join(body_lines).strip() or raw.strip()

    body = _append_source(body, topic)
    keywords = [primary_keyword, *tenant.seo.secondary_keywords]
    return Article(
        title=title,
        seo_title=seo_title,
        meta_description=meta,
        slug=slug,
        body_markdown=body,
        primary_keyword=primary_keyword,
        keywords=keywords,
        topic=topic,
    )


def _append_source(body: str, topic: Topic) -> str:
    """Añade un bloque de fuente al final del artículo si el tema tiene URL de origen."""
    if not topic.source_url:
        return body
    source_name = topic.source_name or topic.source_url
    # Limpia prefijos como "web_search:query" que vienen de WebSearchSource
    if source_name.startswith("web_search:"):
        source_name = source_name.split(":", 1)[1].strip()
    pub_date = topic.published_at.strftime("%d de %B de %Y").lstrip("0") if topic.published_at else ""
    date_str = f", {pub_date}" if pub_date else ""
    return (
        body
        + "\n\n---\n\n"
        + f"**Fuente:** [{source_name}{date_str}]({topic.source_url})"
    )
