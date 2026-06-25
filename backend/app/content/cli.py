"""Interfaz de línea de comandos del motor de contenido.

Uso (desde la carpeta backend/):
    python -m app.content discover --tenant vidra-ia
    python -m app.content run --tenant vidra-ia --dry-run
    python -m app.content run --tenant vidra-ia --no-dry-run --limit 1
"""

from __future__ import annotations

import click
from dotenv import load_dotenv

from app.content import paths
from app.content.config import load_tenant
from app.content.pipeline import Pipeline
from app.content.utils.logging import get_logger

log = get_logger()


def _load_env() -> None:
    """Carga el .env del repo (donde viven ANTHROPIC/OPENAI/LinkedIn)."""
    env_path = paths.env_file()
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  # fallback: busca un .env hacia arriba desde el CWD


@click.group()
def main() -> None:
    """Motor de contenido — genera artículo de blog + autopost en LinkedIn."""
    _load_env()


@main.command()
@click.option("--tenant", required=True, help="Slug del tenant (config/tenants/<slug>.yaml).")
@click.option("--limit", default=5, help="Nº máximo de temas a descubrir.")
def discover(tenant: str, limit: int) -> None:
    """Descubre temas candidatos sin generar ni publicar."""
    cfg = load_tenant(tenant)
    topics = Pipeline(cfg).discover(limit=limit)
    if not topics:
        click.echo("Sin temas.")
        return
    for i, t in enumerate(topics, 1):
        click.echo(f"{i}. [{t.origin.value}] {t.title}  ({t.source_url or '—'})")


@main.command()
@click.option("--tenant", required=True, help="Slug del tenant.")
@click.option("--limit", default=1, help="Nº de piezas a generar en esta ejecución.")
@click.option("--manual", "manual_text", default=None,
              help="Texto de 'algo que hemos hecho' para generar a partir de ello.")
@click.option("--dry-run/--no-dry-run", default=True,
              help="Simular sin publicar ni escribir archivos (por defecto, sí).")
def run(tenant: str, limit: int, manual_text: str | None, dry_run: bool) -> None:
    """Ejecuta el pipeline completo: descubrir -> generar -> SEO -> blog + LinkedIn."""
    cfg = load_tenant(tenant)
    results = Pipeline(cfg, dry_run=dry_run).run(limit=limit, manual_text=manual_text)
    click.echo(f"Hecho. {len(results)} pieza(s) procesada(s). dry_run={dry_run}")


if __name__ == "__main__":
    main()
