"""Generación automática de imagen para cada artículo con gpt-image.

Estética fija: esquema técnico / blueprint (líneas finas navy+cyan sobre fondo claro,
sin texto). Pensada para una cuenta de empresa de I+D, no para marketing.

Flujo:
  1. Haiku redacta un prompt de imagen específico al tema, en estilo blueprint.
  2. gpt-image genera la imagen (1536x1024, horizontal).
  3. La imagen se guarda DIRECTAMENTE en la carpeta pública de la web
     (web/public/images/blog/<slug>.jpg vía app.content.paths).

El path devuelto es relativo a la raíz web (/images/blog/<slug>.jpg)
para insertarlo directamente en el frontmatter del .md.
"""

from __future__ import annotations

import urllib.request

from app.content import paths
from app.content.config import env
from app.content.generation.llm import LLMClient, RESEARCH_MODEL
from app.content.models import Article
from app.content.utils.logging import get_logger

log = get_logger()

# gpt-image-2 es el modelo más reciente de OpenAI (abril 2026); mejor seguimiento
# de instrucciones, incluida la supresión de texto. Tamaño 1536x1024 = landscape.
_IMAGE_MODEL = "gpt-image-2"
_IMAGE_SIZE = "1536x1024"
_IMAGE_QUALITY = "high"


def generate_image(article: Article) -> str | None:
    """Genera la imagen de cabecera del artículo y la guarda en la carpeta pública de la web.

    Devuelve la ruta web relativa (/images/blog/<slug>.jpg)
    o None si falla o no hay clave OpenAI.
    """
    # Clave dedicada del motor (proyecto OpenAI propio, para medir el gasto de imágenes
    # por separado del chatbot). Sin fallback a OPENAI_API_KEY a propósito.
    api_key = env("CONTENT_OPENAI_API_KEY", "")
    if not api_key:
        log.warning("[imagen] CONTENT_OPENAI_API_KEY no configurada — se omite la generación de imagen.")
        return None

    prompt = _build_image_prompt(article)
    if not prompt:
        return None

    log.info("[imagen] Generando imagen (estilo blueprint) con %s para '%s'", _IMAGE_MODEL, article.slug)

    try:
        import openai
    except ImportError:
        log.warning("[imagen] SDK 'openai' no instalado. Ejecuta: pip install openai")
        return None

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.images.generate(
            model=_IMAGE_MODEL,
            prompt=prompt,
            size=_IMAGE_SIZE,
            quality=_IMAGE_QUALITY,
            n=1,
            output_format="jpeg",
        )
    except Exception as exc:
        log.error("[imagen] Error en %s: %s", _IMAGE_MODEL, exc)
        return None

    images_dir = paths.image_dir()
    images_dir.mkdir(parents=True, exist_ok=True)
    local_path = images_dir / f"{article.slug}.jpg"

    try:
        img_data = response.data[0]
        if getattr(img_data, "b64_json", None):
            import base64
            local_path.write_bytes(base64.b64decode(img_data.b64_json))
        elif getattr(img_data, "url", None):
            urllib.request.urlretrieve(img_data.url, local_path)
        else:
            log.error("[imagen] Respuesta sin b64_json ni url.")
            return None
        log.info("[imagen] Guardada en %s", local_path)
    except Exception as exc:
        log.error("[imagen] Error guardando imagen: %s", exc)
        return None

    return f"{paths.image_public_base()}/{article.slug}.jpg"


def _build_image_prompt(article: Article) -> str | None:
    """Usa Haiku para escribir un prompt de imagen específico al concepto técnico del artículo."""
    api_key = env("CONTENT_ANTHROPIC_API_KEY", "")
    if not api_key:
        return _fallback_prompt(article)

    llm = LLMClient(model=RESEARCH_MODEL)

    system = """You are the art director for a technical AI consulting blog. Your job is to write image-generation prompts that are VISUALLY DISTINCT from each other and closely tied to the specific technical concept of each article.

STYLE PALETTE — choose whichever fits the article's concept best (do NOT always pick the same one):

1. ABSTRACT DATA VISUALIZATION — flowing particle streams, glowing data clusters, 3D scatter plots floating in dark space, network topology with luminous edges. Good for: ML models, data pipelines, embeddings, clustering.

2. TECHNICAL SCHEMATIC / BLUEPRINT — thin line drawings, isometric system diagrams, node-and-edge graphs, architecture blocks on a pale background. Good for: system architecture, RAG pipelines, APIs, software infrastructure.

3. CINEMATIC RENDER — dramatic lighting on geometric abstract forms, deep gradients (dark navy to teal/cyan), volumetric depth, clean but evocative. Good for: AI strategy, transformation, business impact articles.

4. MINIMALIST CONCEPT — a single striking visual metaphor rendered with high craft: a precise geometric abstraction, a macro detail, an optical illusion. Good for: explainability, ethics, optimization, decision-making articles.

5. DATA LANDSCAPE — abstract terrain made of data: heatmaps viewed from above, waveforms, probability distributions rendered as 3D surfaces in cool colors. Good for: analytics, forecasting, anomaly detection.

ABSOLUTE PROHIBITIONS (always apply, regardless of style):
- NO text, NO letters, NO numbers, NO labels, NO captions — zero rendered text of any kind (it always comes out garbled).
- NO human faces, NO hands, NO people.
- NO literal robots, NO cartoon brains, NO stock-photo clichés.
- NO logos, NO UI screenshots, NO interfaces.

TECHNICAL QUALITY: photorealistic rendering quality where applicable, sharp focus, professional color grading. Wide 16:9 horizontal composition."""

    prompt = (
        f"Article title: {article.title}\n"
        f"Article description: {article.meta_description}\n"
        f"Primary keyword: {article.primary_keyword}\n\n"
        f"Choose the visual style from the palette above that best represents THIS article's specific "
        f"technical concept. Then write a single detailed image-generation prompt.\n\n"
        f"The image must be unmistakably about the article's specific technical subject — not generic "
        f"'AI vibes'. Think about what the concept actually looks like: a transformer attention mechanism "
        f"looks different from a decision tree, which looks different from a RAG pipeline, which looks "
        f"different from a time-series forecast.\n\n"
        f"Be specific about: the visual forms, the color palette, the lighting/mood, the composition. "
        f"Remind gpt-image that the image must contain NO text, NO numbers, NO labels of any kind. "
        f"Max 200 words. Return only the prompt, no preamble or style label."
    )

    try:
        result = llm.complete(system, prompt, max_tokens=350, model=RESEARCH_MODEL)
        log.debug("[imagen] Prompt de imagen generado por Haiku (%d chars)", len(result))
        return result.strip()
    except Exception as exc:
        log.warning("[imagen] Haiku no pudo generar el prompt: %s — usando prompt genérico.", exc)
        return _fallback_prompt(article)


def _fallback_prompt(article: Article) -> str:
    return (
        f"Abstract technical visualization representing the concept of: {article.primary_keyword}. "
        f"Glowing data streams and geometric network structures floating in deep navy-to-teal space. "
        f"Luminous nodes connected by thin edges, particle clusters suggesting data flow, "
        f"cool cyan and electric blue accents on a dark background. "
        f"Cinematic depth of field, sharp central focus, professional color grading. "
        f"Wide 16:9 horizontal composition. "
        f"Absolutely no text, no numbers, no labels, no human figures, no faces, no logos."
    )
