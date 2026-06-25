"""Plantillas de prompt parametrizadas por el contexto del tenant.

Estilo de referencia: Google AI Blog, NVIDIA Technical Blog, IBM Research, NTT Data Insights.
Principios: precisión técnica, evidencia primero, implementación real, cero hype.
"""

from __future__ import annotations

from app.content.config import TenantConfig
from app.content.models import Topic


def system_prompt(tenant: TenantConfig) -> str:
    b = tenant.brand
    return f"""Eres el lead technical writer e investigador senior de '{tenant.name}'.

IDENTIDAD DE MARCA
Sector: {b.sector}
Audiencia: {b.audience}
Propuesta de valor: {b.value_proposition}
Áreas de expertise: {', '.join(b.expertise)}

POSICIONAMIENTO
Tu escritura es indistinguible de la de Google AI Blog, NVIDIA Technical Blog o IBM Research:
autorizada, técnicamente precisa, respaldada por investigación y accesible a profesionales informados.
La empresa {tenant.name} no comenta la actualidad — la analiza, la contextualiza y muestra cómo implementarla.

PRINCIPIOS IRRENUNCIABLES
1. Insight primero. Abre con el hallazgo o la implicación más importante, nunca con contexto genérico.
2. Precisión técnica. Nombra arquitecturas (GNN, Transformer, CNN, LSTM), cita métricas (RMSE, F1, mAP, IoU), referencia papers y datasets cuando los tengas.
3. Profundidad accesible. Un perfil de negocio debe entenderlo; un ingeniero debe aprender algo nuevo. Usa analogías cuando aclaren un concepto complejo.
4. Evidencia ante todo. Cada afirmación lleva dato, estudio o ejemplo concreto. Sin hype, sin adjetivos vacíos.
5. Orientación a la implementación. Conecta siempre la investigación con lo que una empresa puede hacer hoy, con qué datos, con qué recursos y en qué plazo.
6. Honestidad técnica. Reconoce limitaciones, requisitos de datos y casos donde el método falla. Eso refuerza la credibilidad.
7. Voz institucional pero directa. Sin relleno, sin "en el mundo actual", sin "es fundamental destacar". Frases cortas. Verbos activos.

IDIOMA: {tenant.language} ({tenant.locale}).
"""


def article_prompt(tenant: TenantConfig, topic: Topic, primary_keyword: str) -> str:
    seo = tenant.seo
    source_ref = ""
    if topic.source_url:
        name = topic.source_name or topic.source_url
        source_ref = f"\nFUENTE ORIGINAL: {name} — {topic.source_url}"

    return f"""Redacta un artículo técnico de blog optimizado para SEO a partir de este tema.{source_ref}

TEMA: {topic.title}
CONTEXTO: {topic.summary or topic.raw}

════════════════════════════════════════
ESTRUCTURA OBLIGATORIA
════════════════════════════════════════

H1 — Titular preciso, con la keyword principal, que promete un insight real (no clickbait).
     Estilo: "Redes neuronales gráficas para predecir costes en proyectos" — no "Por qué la IA lo cambiará todo".

INTRO (2-3 párrafos, sin H2) — El problema concreto + por qué las soluciones actuales fallan + qué aporta este enfoque. Sin contexto genérico sobre IA.

H2: El problema técnico en detalle — qué datos, qué variabilidad, qué coste tiene resolverlo mal.

H2: Cómo funciona el método — arquitectura del modelo, pipeline de datos, métricas de evaluación. Incluye analogías cuando aclaren. Si hay benchmarks o comparativas con baseline, cítalos.

H2: Integración práctica — cómo lo adoptaría una empresa hoy: datos necesarios, fases, herramientas compatibles.

H2: Limitaciones y condiciones de uso — qué falla, cuántos datos hacen falta, dónde no aplicar.

H2: Lo que esto significa para el sector — implicación estratégica, ventaja competitiva, cambio de proceso.

CTA final — Una o dos frases que inviten a contactar o explorar más, sin sonar a anuncio. Tono: "Si estás evaluando esta tecnología en tu organización, podemos ayudarte a diseñar el piloto."

════════════════════════════════════════
REQUISITOS SEO
════════════════════════════════════════
- Keyword principal '{primary_keyword}': en H1, en el primer párrafo y de forma natural en el cuerpo.
- Keywords secundarias sugeridas (integrar con naturalidad): {', '.join(seo.secondary_keywords)}.
- Longitud: entre {seo.min_words} y {seo.max_words} palabras.
- Párrafos de máx. 4 líneas. Usa negritas para conceptos técnicos clave la primera vez que aparecen.
- Al menos una lista o tabla donde aporte claridad real (no por obligación).

════════════════════════════════════════
FORMATO DE RESPUESTA (exacto)
════════════════════════════════════════
TITULO: <título visible H1>
SEO_TITLE: <≤60 caracteres, keyword al inicio si es posible>
META: <≤155 caracteres, include keyword, describe el beneficio concreto>
SLUG: <slug-en-minusculas-con-guiones>
CUERPO:
<artículo completo en Markdown>"""


def social_prompt(tenant: TenantConfig, channel: str, article_title: str, summary: str,
                  link: str, fmt: str, hashtags: list[str]) -> str:
    channel_guides = {
        "linkedin": _linkedin_guide(tenant, article_title, summary, link, hashtags),
        "x":        _x_guide(tenant, article_title, summary, link, hashtags),
        "instagram": _instagram_guide(tenant, article_title, summary, link, hashtags),
    }
    return channel_guides.get(channel, _generic_guide(
        tenant, channel, article_title, summary, link, fmt, hashtags
    ))


# ── guías por canal ─────────────────────────────────────────────────────────

def _linkedin_guide(tenant: TenantConfig, title: str, summary: str,
                    link: str, hashtags: list[str]) -> str:
    return f"""Escribe un post de LinkedIn para {tenant.name} a partir de este artículo.

Artículo: {title}
Resumen: {summary}
Enlace: {link}

ESTRUCTURA
1. GANCHO (1 línea) — Una afirmación técnica o dato sorprendente que detenga el scroll. Sin signos de exclamación. Sin "¡Emocionante!". Estilo IBM/NVIDIA: "El 78% de las desviaciones de coste en un proyecto son predecibles dos semanas antes."

2. PROBLEMA (2-3 líneas) — El dolor real que tiene el lector. Lenguaje de responsable de negocio o perfil técnico.

3. QUÉ CAMBIA (3-5 líneas) — El método o hallazgo del artículo. Técnico pero legible. Puede usar formato de lista si son ≥3 puntos.

4. IMPLICACIÓN (1-2 líneas) — Lo que esto significa para el sector o para la empresa del lector.

5. CTA (1 línea) — Invitación a leer, directa y sin hype. "El análisis completo en el enlace."

6. HASHTAGS: {' '.join(hashtags)}

TONO: Voz de investigador senior que comparte un hallazgo relevante con sus pares. Nunca vendedor. Nunca entusiasta vacío.
LONGITUD: 150-250 palabras.
Devuelve solo el texto del post."""


def _x_guide(tenant: TenantConfig, title: str, summary: str,
             link: str, hashtags: list[str]) -> str:
    return f"""Escribe un hilo de X (Twitter) para {tenant.name} a partir de este artículo.

Artículo: {title}
Resumen: {summary}
Enlace: {link}

ESTRUCTURA (4 tweets numerados)
Tweet 1 — Dato o afirmación técnica impactante. Max 240 car. Sin exclamaciones.
Tweet 2 — El método o tecnología en 2-3 frases técnicas pero accesibles.
Tweet 3 — La implicación práctica para el sector.
Tweet 4 — CTA + enlace + hashtags: {' '.join(hashtags)}

Formato de salida:
[1/4] texto
[2/4] texto
[3/4] texto
[4/4] texto {link}

Devuelve solo el hilo."""


def _instagram_guide(tenant: TenantConfig, title: str, summary: str,
                     link: str, hashtags: list[str]) -> str:
    return f"""Escribe el copy para un carrusel de Instagram para {tenant.name}.

Artículo: {title}
Resumen: {summary}

ESTRUCTURA
Slide 1 (portada): Titular impactante ≤8 palabras. Sin emojis en exceso.
Slides 2-5: Un concepto clave por slide. Frase corta + dato o métrica.
Slide 6 (cierre): CTA + "Más en nuestra web" + bio link.

Caption del post (bajo la imagen): 80-100 palabras, tono técnico-accesible.
Hashtags al final: {' '.join(hashtags)}

Devuelve: los textos de cada slide numerados y el caption separado."""


def _generic_guide(tenant: TenantConfig, channel: str, title: str, summary: str,
                   link: str, fmt: str, hashtags: list[str]) -> str:
    return (
        f"Adapta este artículo a {channel} para {tenant.name}.\n"
        f"Formato: {fmt}.\nTítulo: {title}\nResumen: {summary}\nEnlace: {link}\n"
        f"Hashtags: {' '.join(hashtags)}\n\n"
        "Tono: técnico, directo, sin hype. Devuelve solo el texto."
    )
