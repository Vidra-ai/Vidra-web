"""Resolución central de rutas del motor de contenido.

El motor vive en `backend/app/content/` pero escribe en el árbol de la web
(`web/src/content/blog` y `web/public/images/blog`), todo dentro del mismo repo.
Cada ruta es configurable por variable de entorno; el valor por defecto se
calcula relativo a la raíz del repositorio para que funcione sin configuración.
"""

from __future__ import annotations

import os
from pathlib import Path

# backend/app/content/paths.py
#   parents[0] = content   parents[1] = app   parents[2] = backend   parents[3] = raíz del repo
BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = Path(__file__).resolve().parents[3]


def _env_path(name: str, default: Path) -> Path:
    value = os.environ.get(name, "").strip()
    return Path(value) if value else default


def tenants_dir() -> Path:
    """Carpeta con los YAML de tenants (config/tenants/<slug>.yaml)."""
    return _env_path("CONTENT_TENANTS_DIR", BACKEND_ROOT / "config" / "tenants")


def blog_dir() -> Path:
    """Carpeta de artículos del blog Astro donde se deposita el .md generado."""
    return _env_path("CONTENT_BLOG_DIR", REPO_ROOT / "web" / "src" / "content" / "blog")


def image_dir() -> Path:
    """Carpeta pública de la web donde se guarda la imagen de cabecera."""
    return _env_path("CONTENT_IMAGE_DIR", REPO_ROOT / "web" / "public" / "images" / "blog")


def image_public_base() -> str:
    """Prefijo web de la imagen para el frontmatter del .md (p. ej. /images/blog)."""
    return os.environ.get("CONTENT_IMAGE_PUBLIC_BASE", "/images/blog").rstrip("/")


def output_dir() -> Path:
    """Carpeta de salida para el JSON del resultado y el histórico anti-repetición."""
    return _env_path("CONTENT_OUTPUT_DIR", BACKEND_ROOT / "content_output")


def env_file() -> Path:
    """Ruta del .env del repo (para cargar/persistir credenciales como el token de LinkedIn)."""
    return REPO_ROOT / ".env"
