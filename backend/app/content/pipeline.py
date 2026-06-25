"""Orquestador: descubrir -> evaluar -> generar -> SEO -> publicar/coordinar.

Escribe el artículo y la imagen directamente en el árbol de la web del repo
(ver app.content.paths) y, opcionalmente, autopostea en LinkedIn.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from app.content import paths
from app.content.config import TenantConfig
from app.content.generation import ContentGenerator
from app.content.generation.image import generate_image
from app.content.generation.translator import translate_to_english
from app.content.models import Article, PublishResult, SocialVariant, Topic
from app.content.publishers import REGISTRY
from app.content.sources import ManualSource, RssSource
from app.content.sources.web_search import WebSearchSource
from app.content.utils.logging import get_logger

log = get_logger()

CANDIDATES_PER_POST = 10


def _step(msg: str) -> float:
    """Imprime un paso del pipeline con timestamp y devuelve el tiempo de inicio."""
    import datetime
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\n[{ts}] {msg}", flush=True)
    return time.time()


def _done(t0: float, extra: str = "") -> None:
    elapsed = time.time() - t0
    suffix = f"  {extra}" if extra else ""
    print(f"         -> listo en {elapsed:.1f}s{suffix}", flush=True)


class Pipeline:
    def __init__(self, tenant: TenantConfig, dry_run: bool = True) -> None:
        self.tenant = tenant
        self.dry_run = dry_run
        self.generator = ContentGenerator(tenant)
        self.output_dir = paths.output_dir() / tenant.slug

    # --- historial de publicados -------------------------------------------
    def _published_path(self) -> Path:
        return self.output_dir / "published.json"

    def _load_published(self) -> list[str]:
        path = self._published_path()
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return []

    def _save_published(self, titles: list[str]) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._published_path().write_text(
            json.dumps(titles, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # --- etapas ------------------------------------------------------------
    def discover(self, limit: int = 5, manual_text: str | None = None) -> list[Topic]:
        if manual_text:
            return ManualSource(self.tenant, text=manual_text).discover()

        topics = RssSource(self.tenant).discover(limit=limit)

        if not topics and self.tenant.sources.web_search_fallback:
            log.info("RSS sin resultados — activando búsqueda web con Haiku.")
            topics = WebSearchSource(self.tenant).discover(limit=limit)

        return topics

    def run(self, limit: int = 1, manual_text: str | None = None) -> list[dict]:
        print(f"\n{'='*55}", flush=True)
        print(f"  Content engine — tenant: {self.tenant.slug}  |  dry_run: {self.dry_run}", flush=True)
        print(f"{'='*55}", flush=True)

        published_titles = self._load_published()
        print(f"  Historial: {len(published_titles)} articulos ya publicados", flush=True)

        if manual_text:
            topics = ManualSource(self.tenant, text=manual_text).discover()
            ranked = topics
        else:
            t0 = _step("PASO 1/4  Buscando noticias (ultimos 3 dias)...")
            candidates_needed = limit * CANDIDATES_PER_POST
            candidates = self.discover(limit=candidates_needed)
            if not candidates:
                print("  -> Sin resultados. Comprueba los feeds RSS o activa web_search.", flush=True)
                log.warning("No se han encontrado temas para '%s'.", self.tenant.slug)
                return []
            _done(t0, f"{len(candidates)} candidatos encontrados")

            t0 = _step(f"PASO 2/4  Haiku evalua {len(candidates)} candidatos y elige el mejor...")
            ranked = self.generator.evaluate_topics(candidates, published_titles)
            _done(t0, f"tema elegido: \"{ranked[0].title[:70]}...\"" if ranked else "sin ranking")

        results = []
        used_titles = list(published_titles)
        for topic in ranked[:limit]:
            t0 = _step("PASO 3/4  El modelo redacta el articulo (puede tardar 1-2 min)...")
            print(f"         Tema: {topic.title[:80]}", flush=True)
            article = self.generator.generate_article(topic)
            _done(t0, f"{len(article.body_markdown.split())} palabras — \"{article.title[:60]}\"")

            if not self.dry_run:
                t0 = _step("PASO 3b   Generando imagen con gpt-image...")
                image_path = generate_image(article)
                _done(t0, image_path or "FALLO — se continua sin imagen")
            else:
                image_path = None
                print("\n         [dry-run] Imagen omitida", flush=True)

            t0 = _step("PASO 3c   Traduciendo al inglés con Haiku...")
            translated = translate_to_english(article, self.generator.llm) if not self.dry_run else None
            if translated:
                _done(t0, f"EN slug: {translated['slug']}")
            else:
                _done(t0, "[dry-run]" if self.dry_run else "FALLO — se continúa sin versión EN")

            t0 = _step("PASO 4/4  Publicando y guardando archivos...")
            web_result = self._publish_web(article, image_path=image_path)
            if translated and not self.dry_run:
                self._publish_web_en(article, translated, image_path=image_path)
            link = self._article_url(article)
            variants = self.generator.generate_social_variants(article, link)
            social_results = self._publish_social(variants)
            record = self._persist(article, variants, web_result, social_results)
            results.append(record)
            used_titles.append(article.title)

            out_md = paths.blog_dir() / f"{article.slug}.md"
            out_img = paths.image_dir() / f"{article.slug}.jpg"
            _done(t0)
            print("\n  RESULTADO:", flush=True)
            print(f"  Articulo ES -> {out_md}", flush=True)
            if translated and not self.dry_run:
                out_md_en = paths.blog_dir() / f"{translated['slug']}.md"
                print(f"  Articulo EN -> {out_md_en}", flush=True)
            if image_path:
                print(f"  Imagen      -> {out_img}", flush=True)
            for r in social_results:
                estado = "OK" if r.success else "FALLO (texto guardado para pegar a mano)"
                print(f"  {r.channel:<12} -> {estado}  {r.message[:60]}", flush=True)
                social_txt = self.output_dir / f"{article.slug}.{r.channel}.txt"
                print(f"  {'':<12}    texto -> {social_txt}", flush=True)

        self._save_published(used_titles)
        print(f"\n{'='*55}\n", flush=True)
        return results

    # --- publicación -------------------------------------------------------
    def _article_url(self, article: Article) -> str:
        """URL pública (absoluta) del artículo, para enlazar desde RRSS.

        Se construye a partir de seo.internal_links_base (p. ej.
        https://vidra-ia.com/blog) + slug. Si no hay base configurada, se
        devuelve la ruta relativa /blog/<slug>.

        OJO: al autopostear justo tras generar, el artículo aún no está
        desplegado. Publica en LinkedIn cuando la web esté en producción
        (o usa --dry-run para revisar el post antes).
        """
        base = (self.tenant.seo.internal_links_base or "").rstrip("/")
        if base:
            return f"{base}/{article.slug}"
        return f"/blog/{article.slug}"

    def _publish_web(self, article: Article, image_path: str | None = None) -> PublishResult:
        if self.tenant.channel_enabled("vidra_md"):
            md_result = REGISTRY["vidra_md"](self.tenant, dry_run=self.dry_run).publish_article(
                article, image_path=image_path
            )
            log.info("[vidra_md] %s", md_result.message)
            return md_result

        return PublishResult(channel="vidra_md", success=False,
                             message="Canal web (vidra_md) desactivado para este tenant.")

    def _publish_web_en(self, article: Article, translated: dict, image_path: str | None = None) -> None:
        """Escribe la versión inglesa del artículo en web/src/content/blog/<en-slug>.md."""
        from datetime import date
        from app.content.publishers.vidra_md import _pick_category

        out_dir = paths.blog_dir()
        category = _pick_category(article)
        today = date.today().isoformat()
        image = image_path or f"{paths.image_public_base()}/{article.slug}.jpg"

        en_title = translated["title"].replace('"', '\\"')
        en_desc = translated["meta_description"].replace('"', '\\"')
        en_slug = translated["slug"]

        content = (
            f'---\n'
            f'title: "{en_title}"\n'
            f'description: "{en_desc}"\n'
            f'pubDate: "{today}"\n'
            f'lang: "en"\n'
            f'category: "{category}"\n'
            f'translationKey: "{article.slug}"\n'
            f'image: "{image}"\n'
            f'---\n\n'
            f'{translated["body_markdown"]}\n'
        )

        out = out_dir / f"{en_slug}.md"
        out_dir.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        log.info("[vidra_md_en] Escrito %s", out)
        print(f"  EN versión -> {out}", flush=True)

    def _publish_social(self, variants: list[SocialVariant]) -> list[PublishResult]:
        results = []
        for variant in variants:
            cls = REGISTRY.get(variant.channel)
            if not cls:
                continue
            result = cls(self.tenant, dry_run=self.dry_run).publish_social(variant)
            log.info("[%s] %s", variant.channel, result.message)
            results.append(result)
        return results

    # --- persistencia ------------------------------------------------------
    def _persist(self, article, variants, web_result, social_results) -> dict:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "tenant": self.tenant.slug,
            "dry_run": self.dry_run,
            "article": article.model_dump(),
            "variants": [v.model_dump() for v in variants],
            "web_result": web_result.model_dump(),
            "social_results": [r.model_dump() for r in social_results],
        }
        out = self.output_dir / f"{article.slug}.json"
        out.write_text(json.dumps(record, ensure_ascii=False, indent=2, default=str),
                       encoding="utf-8")
        log.info("Output guardado en %s", out)

        # Volca el texto de cada variante social a un .txt aparte, listo para copiar
        # y pegar a mano. Imprescindible mientras el autopost de LinkedIn no esté
        # operativo (token / aprobación de la Community Management API pendiente).
        for variant in variants:
            tags = " ".join(h if h.startswith("#") else f"#{h}" for h in variant.hashtags)
            txt = f"{variant.text}\n\n{tags}".strip()
            if variant.link:
                txt += f"\n\n{variant.link}"
            social_out = self.output_dir / f"{article.slug}.{variant.channel}.txt"
            social_out.write_text(txt + "\n", encoding="utf-8")
            log.info("Texto social (%s) guardado en %s", variant.channel, social_out)

        return record
