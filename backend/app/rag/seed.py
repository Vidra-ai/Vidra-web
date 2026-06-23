"""Carga inicial y sincronización diaria de documentos del RAG.

- seed_documents(): indexa archivos locales de backend/RAG/ (una sola vez por archivo).
- sync_remote_sources(): descarga URLs de backend/RAG/sources.yml y re-indexa
  solo las que hayan cambiado (hash SHA-256). Si sources.yml está vacío, no hace nada.

Uso manual:

    docker compose exec api python -m app.rag.seed
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import httpx
import yaml
from sqlalchemy import select

from app.db import init_db, session_scope
from app.models import RagDocument
from app.rag.ingest import ingest_document

_DOCS_DIR = Path(__file__).parent.parent.parent / "RAG"
_SOURCES_FILE = _DOCS_DIR / "sources.yml"
_HASH_CACHE = _DOCS_DIR / ".sources_hashes.json"


def _load_hash_cache() -> dict[str, str]:
    if _HASH_CACHE.exists():
        return json.loads(_HASH_CACHE.read_text())
    return {}


def _save_hash_cache(cache: dict[str, str]) -> None:
    _HASH_CACHE.write_text(json.dumps(cache, indent=2))


def _load_sources() -> list[dict]:
    if not _SOURCES_FILE.exists():
        return []
    data = yaml.safe_load(_SOURCES_FILE.read_text(encoding="utf-8")) or {}
    return data.get("sources") or []


def sync_remote_sources() -> None:
    """Descarga fuentes remotas de sources.yml y re-indexa solo las que hayan cambiado."""
    sources = _load_sources()
    if not sources:
        return

    init_db()
    hash_cache = _load_hash_cache()
    changed = 0

    with session_scope() as session:
        for src in sources:
            url = str(src["url"])
            titulo = src["titulo"]
            tipo = src.get("tipo")
            area = src.get("area")

            try:
                response = httpx.get(url, follow_redirects=True, timeout=30.0)
                response.raise_for_status()
                content = response.content
                new_hash = hashlib.sha256(content).hexdigest()

                if hash_cache.get(url) == new_hash:
                    continue

                old_doc = session.execute(
                    select(RagDocument).where(RagDocument.fuente_original == url)
                ).scalar_one_or_none()
                if old_doc:
                    session.delete(old_doc)
                    session.flush()

                result = ingest_document(session, content, url, titulo, tipo, area)
                hash_cache[url] = new_hash
                _save_hash_cache(hash_cache)
                changed += 1
                print(f"[sync] ✓ {titulo} — {result.chunks} chunks actualizados")

            except Exception as exc:
                print(f"[sync] ✗ {titulo} ({url}): {exc}", file=sys.stderr)

    if changed == 0:
        print("[sync] Sin cambios en fuentes remotas.")


def seed_documents() -> None:
    """Indexa archivos locales nuevos de backend/RAG/. Idempotente."""
    if not _DOCS_DIR.exists():
        print(f"Carpeta no encontrada: {_DOCS_DIR}")
        return

    files = sorted(
        f for f in _DOCS_DIR.rglob("*")
        if f.is_file()
        and f.suffix.lower() in {".pdf", ".txt", ".docx", ".xlsx", ".xls"}
        and not f.name.startswith(("~$", "."))
    )

    init_db()
    with session_scope() as session:
        already_indexed = {
            doc.fuente_original
            for doc in session.execute(select(RagDocument)).scalars().all()
        }
        pending = [f for f in files if f.name not in already_indexed]

        if not pending:
            print("Archivos locales: todos ya indexados.")
        else:
            print(f"Indexando {len(pending)} archivo(s) local(es)...")
            for filepath in pending:
                try:
                    content = filepath.read_bytes()
                    result = ingest_document(
                        session,
                        content,
                        filepath.name,
                        titulo=filepath.stem.replace("_", " ").replace("-", " ").title(),
                    )
                    print(f"  ✓ {result.titulo} — {result.chunks} chunks")
                except Exception as exc:
                    print(f"  ✗ {filepath.name}: {exc}", file=sys.stderr)

    sync_remote_sources()
    print("Seed completado.")


if __name__ == "__main__":
    try:
        seed_documents()
    except Exception as exc:
        print(f"Error durante el seed: {exc}", file=sys.stderr)
        sys.exit(1)
