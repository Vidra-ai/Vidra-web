# Motor de contenido (`app.content`)

Funcionalidad de la web que **genera un artículo de blog optimizado para SEO** con
Claude (+ imagen de cabecera con gpt-image) y **autopostea en LinkedIn**. Es el
proyecto *ContentPilot* encapsulado dentro de este repo, recortado a lo necesario:
solo los canales **blog (`vidra_md`)** y **LinkedIn**.

## Cómo funciona

```
sources/      → descubre temas (RSS del sector + búsqueda web con Haiku) o entrada manual
generation/   → Claude redacta el artículo (SEO) + variantes sociales; gpt-image crea la imagen
publishers/   → vidra_md (escribe el .md en el blog) + linkedin (autopost)
pipeline.py   → orquesta: descubrir → evaluar → redactar → imagen → escribir blog → LinkedIn
config.py     → carga el tenant (config/tenants/<slug>.yaml) + secretos de entorno
paths.py      → resuelve dónde escribir (árbol de la web del repo)
```

A diferencia del proyecto original (que dejaba todo en una carpeta `output/`), aquí el
motor vive **dentro del repo de la web**, así que escribe directamente en:

| Salida | Ruta (por defecto) |
|--------|--------------------|
| Artículo `.md` | `web/src/content/blog/<slug>.md` |
| Imagen de cabecera | `web/public/images/blog/<slug>.jpg` |
| JSON + histórico + textos sociales | `backend/content_output/<tenant>/` (gitignored) |

El frontmatter del `.md` es compatible con `web/src/content.config.ts`
(`title, description, pubDate, lang, category, translationKey, image`).

**Flujo real:** ejecutas el motor en local → genera el `.md` + la imagen en el repo y
autopostea en LinkedIn → **revisas y haces `git commit`** → la web se reconstruye y
publica el artículo. (El contenedor de producción no monta el repo de la web; por eso
el motor es de uso local + commit, no un endpoint en producción.)

## Uso

Desde la carpeta `backend/` (con el `.env` del repo relleno):

```bash
# Solo descubrir temas (no genera ni publica)
python -m app.content discover --tenant vidra-ia

# Simulación: redacta el artículo pero NO escribe archivos ni publica
python -m app.content run --tenant vidra-ia --dry-run

# Real: escribe el .md + imagen en el repo e intenta autopostear en LinkedIn
python -m app.content run --tenant vidra-ia --no-dry-run --limit 1

# A partir de una nota propia ("lo que hemos hecho")
python -m app.content run --tenant vidra-ia --no-dry-run \
  --manual "Hemos implantado un asistente RAG para el área legal de un cliente..."
```

Dependencias: `pip install -r backend/requirements.txt` (añade `anthropic, openai,
feedparser, python-slugify, click, python-dotenv`).

## Estado de LinkedIn ⚠️

**El autopost en LinkedIn NO está operativo todavía**: el token está caducado y la
publicación como organización está pendiente de la aprobación de la *Community
Management API*. El pipeline lo gestiona con elegancia:

- El artículo y la imagen se escriben **antes** de tocar LinkedIn; un fallo de LinkedIn
  **no** rompe la generación.
- El **texto del post se genera y se guarda igualmente** en
  `backend/content_output/<tenant>/<slug>.linkedin.txt`, listo para **pegarlo a mano**.

Cuando se desbloquee, ejecuta `python backend/scripts/linkedin_auth.py` para obtener un
token nuevo y rellena `LINKEDIN_AUTHOR_URN` en el `.env`. El refresco del token es
automático a partir de ahí.

## Configuración (tenant)

Cada "cliente/marca" es un *tenant* en `backend/config/tenants/<slug>.yaml`:

- `vidra-ia.yaml` — el de la web de Vidra (revísalo: keywords, fuentes y tono definen el
  contenido). Solo LinkedIn activo como red social.
- `construccion-ia.yaml` — ejemplo de referencia para dar de alta otro sector.

Los secretos (claves API, token de LinkedIn) **nunca** van en el YAML: van en el `.env`
del repo. Variables:

- `CONTENT_ANTHROPIC_API_KEY` — Claude: redacción, evaluación, post de LinkedIn y prompt de imagen.
- `CONTENT_OPENAI_API_KEY` — gpt-image: imagen de cabecera.
- `CONTENT_LLM_MODEL`, `LINKEDIN_*`, `CLIENT_ID/SECRET` y los `CONTENT_*` opcionales de rutas.

Las dos claves de API son **dedicadas** (proyectos propios, separadas de las del chatbot)
para poder medir el gasto del motor por separado. No hay fallback a las claves del
chatbot: si están vacías, el motor no genera. Ver `.env.example`.
