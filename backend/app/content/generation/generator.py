"""Orquesta la generación: tema -> artículo SEO -> variantes por canal.

Estrategia de modelos:
  - Investigación / enriquecimiento del tema: RESEARCH_MODEL (Haiku) — rápido y barato.
  - Redacción del artículo y variantes RRSS: WRITING_MODEL (Sonnet/Opus) — máxima calidad.
"""

from __future__ import annotations

from app.content.config import TenantConfig
from app.content.generation import prompts, seo
from app.content.generation.llm import LLMClient, RESEARCH_MODEL, WRITING_MODEL
from app.content.models import Article, SocialVariant, Topic
from app.content.utils.logging import get_logger

log = get_logger()


class ContentGenerator:
    def __init__(self, tenant: TenantConfig, llm: LLMClient | None = None) -> None:
        self.tenant = tenant
        # Un único cliente; el modelo por defecto es WRITING_MODEL.
        # Los pasos de investigación pasan model=RESEARCH_MODEL explícitamente.
        self.llm = llm or LLMClient(model=WRITING_MODEL)

    def enrich_topic(self, topic: Topic) -> Topic:
        """Usa Haiku para extraer un resumen estructurado del tema antes de redactar."""
        if not topic.summary:
            return topic
        system = "Eres un asistente de investigación de contenido. Responde siempre en español."
        prompt = (
            f"Analiza esta noticia y extrae en 3-5 frases los puntos clave más relevantes "
            f"para una audiencia del sector '{self.tenant.brand.sector}'.\n\n"
            f"Título: {topic.title}\nResumen: {topic.summary}"
        )
        enriched_summary = self.llm.complete(
            system, prompt, max_tokens=512, model=RESEARCH_MODEL
        )
        log.info("Tema enriquecido con Haiku (%d chars)", len(enriched_summary))
        return topic.model_copy(update={"raw": enriched_summary})

    def evaluate_topics(self, candidates: list[Topic], published_titles: list[str]) -> list[Topic]:
        """Usa Haiku para valorar N candidatos y devuelve la lista ordenada de mejor a peor.

        Descarta automáticamente temas ya cubiertos (por título similar).
        """
        if not candidates:
            return []

        published_block = "\n".join(f"- {t}" for t in published_titles) if published_titles else "(ninguno)"
        topics_block = "\n".join(
            f"{i+1}. [{t.source_name or 'sin fuente'}] {t.title} — {t.summary or ''}"
            for i, t in enumerate(candidates)
        )
        system = "Eres un editor de contenido SEO especializado en tecnología e inteligencia artificial. Responde SOLO con los números en orden, separados por comas. Sin explicación."
        prompt = (
            f"Sector: {self.tenant.brand.sector}\n"
            f"Audiencia: {self.tenant.brand.audience}\n\n"
            f"Artículos ya publicados (no repetir):\n{published_block}\n\n"
            f"Candidatos:\n{topics_block}\n\n"
            f"Ordena los candidatos de más a menos interesante para publicar ahora. "
            f"Criterios: novedad, relevancia para la audiencia, diferenciación respecto a lo ya publicado, potencial SEO. "
            f"Responde solo con los números separados por comas. Ejemplo: 3,1,5,2,4"
        )
        raw = self.llm.complete(system, prompt, max_tokens=64, model=RESEARCH_MODEL)
        log.info("Evaluación de temas (Haiku): %s", raw.strip())

        try:
            order = [int(x.strip()) - 1 for x in raw.strip().split(",") if x.strip().isdigit()]
            ranked = [candidates[i] for i in order if 0 <= i < len(candidates)]
            # añade los que Haiku no haya incluido al final
            included = set(order)
            ranked += [c for i, c in enumerate(candidates) if i not in included]
            return ranked
        except Exception:
            log.warning("No se pudo parsear el ranking de Haiku; usando orden original.")
            return candidates

    def generate_article(self, topic: Topic) -> Article:
        enriched = self.enrich_topic(topic)
        primary = seo.pick_primary_keyword(self.tenant, enriched)
        log.info("Redactando artículo con %s (keyword: '%s')", WRITING_MODEL, primary)
        system = prompts.system_prompt(self.tenant)
        prompt = prompts.article_prompt(self.tenant, enriched, primary)
        raw = self.llm.complete(system, prompt, max_tokens=64000, model=WRITING_MODEL)
        if not raw.strip():
            log.error("El LLM devolvió respuesta vacía para el tema: %s", topic.title)
            raise RuntimeError(f"LLM devolvió respuesta vacía para: {topic.title}")
        log.debug("LLM output: %d chars, primer bloque: %s", len(raw), raw[:120])
        return seo.parse_article(raw, self.tenant, enriched, primary)

    def generate_social_variants(self, article: Article, link: str) -> list[SocialVariant]:
        variants: list[SocialVariant] = []
        system = prompts.system_prompt(self.tenant)
        for channel, cfg in self.tenant.channels.items():
            if channel in ("wordpress", "vidra_md") or not cfg.get("enabled"):
                continue
            hashtags = cfg.get("hashtags", [])
            fmt = cfg.get("format", "")
            prompt = prompts.social_prompt(
                self.tenant, channel, article.title,
                article.meta_description, link, fmt, hashtags,
            )
            # Variantes RRSS: WRITING_MODEL para calidad; si se quisiera ahorrar se puede
            # cambiar a RESEARCH_MODEL para posts cortos.
            text = self.llm.complete(system, prompt, max_tokens=4096, model=WRITING_MODEL)
            variants.append(
                SocialVariant(channel=channel, text=text.strip(),
                              hashtags=hashtags, link=link)
            )
        return variants
