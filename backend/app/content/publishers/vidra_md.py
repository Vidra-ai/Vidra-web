"""Genera el artículo como .md y lo deposita en el blog Astro de Vidra.

A diferencia del ContentPilot original (que escribía en una carpeta output/
independiente), aquí el motor vive dentro del propio repo de la web, así que el
.md se escribe DIRECTAMENTE en web/src/content/blog/<slug>.md (vía
app.content.paths). El frontmatter es compatible con web/src/content.config.ts.

Flujo de publicación: el motor genera el .md + la imagen en el repo; tú revisas y
haces commit -> la web se reconstruye y publica el artículo.
"""

from __future__ import annotations

from datetime import date

from app.content import paths
from app.content.models import Article, PublishResult, SocialVariant
from app.content.publishers.base import BasePublisher
from app.content.utils.logging import get_logger

log = get_logger()

# Categorías válidas según web/src/content.config.ts:
#   analytics | machine-learning | deep-learning | empresa
_CATEGORY_MAP = {
    "machine learning":    "machine-learning",
    "aprendizaje automático": "machine-learning",
    "deep learning":       "deep-learning",
    "redes neuronales":    "deep-learning",
    "neural":              "deep-learning",
    "predicción":          "machine-learning",
    "análisis":            "analytics",
    "analytics":           "analytics",
    "datos":               "analytics",
}
_DEFAULT_CATEGORY = "analytics"


class VidraMdPublisher(BasePublisher):
    """Escribe el artículo como .md con frontmatter de Vidra en web/src/content/blog/."""

    channel = "vidra_md"

    def publish_article(self, article: Article, image_path: str | None = None) -> PublishResult:
        out_dir = paths.blog_dir()

        category = _pick_category(article)
        today = date.today().isoformat()
        content = _render_md(article, category, today, image_path)

        out = out_dir / f"{article.slug}.md"

        if self.dry_run:
            log.info("[vidra_md] [DRY-RUN] Generaría %s", out)
            return PublishResult(
                channel="vidra_md", success=True, dry_run=True,
                message=f"[DRY-RUN] Generaría {out}",
            )

        out_dir.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        log.info("[vidra_md] Escrito %s", out)
        return PublishResult(
            channel="vidra_md", success=True, dry_run=False,
            url=f"/blog/{article.slug}",
            message=f"Escrito {out}",
        )

    def publish_social(self, variant: SocialVariant) -> PublishResult:
        return PublishResult(channel="vidra_md", success=True, dry_run=self.dry_run,
                             message="vidra_md no gestiona variantes sociales.")


def _pick_category(article: Article) -> str:
    blob = f"{article.title} {article.primary_keyword} {' '.join(article.keywords)}".lower()
    for kw, cat in _CATEGORY_MAP.items():
        if kw in blob:
            return cat
    return _DEFAULT_CATEGORY


def _render_md(article: Article, category: str, today: str, image_path: str | None = None) -> str:
    title = article.title.replace('"', '\\"')
    desc = article.meta_description.replace('"', '\\"')
    image = image_path or f"{paths.image_public_base()}/{article.slug}.jpg"

    return (
        f'---\n'
        f'title: "{title}"\n'
        f'description: "{desc}"\n'
        f'pubDate: "{today}"\n'
        f'lang: "es"\n'
        f'category: "{category}"\n'
        f'translationKey: "{article.slug}"\n'
        f'image: "{image}"\n'
        f'---\n\n'
        f'{article.body_markdown}\n'
    )
