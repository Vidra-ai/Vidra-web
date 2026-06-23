"""Sincronización incremental de la carpeta pública de Obsidian.

Lee los .md de la carpeta "Información pública" del vault (montada solo lectura) y
mantiene el índice RAG al día re-embebiendo SOLO los ficheros que cambian:

- Fichero nuevo            → se indexa.
- Fichero modificado       → se borra su documento y se re-indexa (hash distinto).
- Fichero sin cambios      → se omite (mismo hash).
- Fichero borrado / privado→ se elimina del índice.

Solo se indexan notas con frontmatter `visibilidad: publico` (ADR-005), salvo que
se desactive con PUBLIC_DOCS_REQUIRE_PUBLIC_FLAG=false.

Los documentos gestionados por esta sincronización se identifican por el prefijo
`obsidian://` en `fuente_original`, para no interferir con subidas manuales ni
fuentes remotas.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import session_scope
from app.models import RagDocument
from app.rag.ingest import clean_markdown, ingest_text
from app.settings import get_settings

_SENTINEL = "obsidian://"


def _public_dir() -> Path | None:
    raw = get_settings().public_docs_dir.strip()
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_dir() else None


def _delete_doc(session: Session, fuente: str) -> None:
    doc = session.execute(
        select(RagDocument).where(RagDocument.fuente_original == fuente)
    ).scalar_one_or_none()
    if doc:
        session.delete(doc)
        session.commit()


def sync_public_docs() -> dict:
    """Sincroniza la carpeta pública con el índice. Idempotente y de bajo coste:
    solo embebe los ficheros cuyo contenido ha cambiado."""
    settings = get_settings()
    summary = {"indexed": 0, "updated": 0, "unchanged": 0, "removed": 0,
               "skipped_private": 0, "errors": 0}

    base = _public_dir()
    if base is None:
        return summary

    require_public = settings.public_docs_require_public_flag

    with session_scope() as session:
        # Estado actual en la DB de los documentos gestionados desde Obsidian.
        managed = {
            doc.fuente_original: doc.content_hash
            for doc in session.execute(
                select(RagDocument).where(RagDocument.fuente_original.like(f"{_SENTINEL}%"))
            ).scalars().all()
        }
        seen: set[str] = set()

        for filepath in sorted(base.rglob("*.md")):
            if filepath.name.startswith("."):
                continue
            rel = filepath.relative_to(base).as_posix()
            fuente = f"{_SENTINEL}{rel}"

            try:
                raw_bytes = filepath.read_bytes()
                new_hash = hashlib.sha256(raw_bytes).hexdigest()
                meta, body = clean_markdown(raw_bytes.decode("utf-8", errors="replace"))

                is_public = str(meta.get("visibilidad", "")).lower() == "publico"
                if require_public and not is_public:
                    summary["skipped_private"] += 1
                    if fuente in managed:  # dejó de ser pública: retírala
                        _delete_doc(session, fuente)
                        summary["removed"] += 1
                    continue

                if not body.strip():  # nota vacía: trátala como ausente
                    if fuente in managed:
                        _delete_doc(session, fuente)
                        summary["removed"] += 1
                    continue

                seen.add(fuente)

                if managed.get(fuente) == new_hash:
                    summary["unchanged"] += 1
                    continue

                existed = fuente in managed
                if existed:
                    _delete_doc(session, fuente)

                ingest_text(
                    session,
                    text=body,
                    titulo=filepath.stem,
                    fuente=fuente,
                    tipo="obsidian",
                    area=None,
                    content_hash=new_hash,
                    nivel_confidencialidad="publico",
                )
                summary["updated" if existed else "indexed"] += 1
                print(f"[public-docs] {'↻' if existed else '＋'} {rel}")

            except Exception as exc:
                session.rollback()  # no dejar estado a medias para el commit final
                summary["errors"] += 1
                print(f"[public-docs] ✗ {rel}: {exc}", file=sys.stderr)

        # Elimina del índice los documentos cuyo fichero ya no existe.
        for fuente in managed:
            if fuente not in seen:
                # 'seen' solo contiene ficheros públicos presentes; los privados ya se
                # gestionaron arriba. Aquí caen los realmente borrados del disco.
                if not (base / fuente[len(_SENTINEL):]).exists():
                    _delete_doc(session, fuente)
                    summary["removed"] += 1

    return summary
