"""Recuperación híbrida sobre los chunks indexados.

Combina dos rankings independientes y los fusiona con Reciprocal Rank Fusion (RRF):
  1. Vectorial — similitud semántica (coseno sobre embeddings).
  2. Léxica   — similitud de trigramas (pg_trgm) insensible a acentos (unaccent).
"""

from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models import RagChunk, RagDocument
from app.rag.embedder import embed_one
from app.rag.normalize import expand_abbreviations
from app.rag.schemas import ChatSource

_CANDIDATES = 40
_RRF_K = 60


def _extract_section(texto: str) -> str | None:
    """Devuelve el primer encabezado de sección (línea en MAYÚSCULAS) del chunk."""
    for line in texto.splitlines():
        line = line.strip()
        if line.startswith("[Hoja:"):
            continue
        if len(line) >= 4 and line == line.upper() and any(c.isalpha() for c in line):
            return line.title()
    return None


def _vector_ranking(session: Session, query_vec: list[float]) -> list[int]:
    stmt = (
        select(RagChunk.id, RagChunk.embedding.cosine_distance(query_vec).label("dist"))
        .where(RagChunk.embedding.is_not(None))
        .order_by("dist")
        .limit(_CANDIDATES)
    )
    return [row.id for row in session.execute(stmt).all()]


def _lexical_ranking(session: Session, query: str) -> list[int]:
    stmt = text(
        """
        SELECT id
        FROM rag_chunks
        WHERE embedding IS NOT NULL
        ORDER BY word_similarity(unaccent(lower(:q)), unaccent(lower(texto))) DESC
        LIMIT :n
        """
    )
    return [row[0] for row in session.execute(stmt, {"q": query, "n": _CANDIDATES})]


def _fuse(rankings: list[list[int]]) -> list[int]:
    """Reciprocal Rank Fusion: combina varios rankings en uno solo."""
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, cid in enumerate(ranking):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (_RRF_K + rank)
    return sorted(scores, key=lambda cid: scores[cid], reverse=True)


def retrieve(session: Session, pregunta: str, top_k: int = 10) -> list[ChatSource]:
    expanded = expand_abbreviations(pregunta)
    query_vec = embed_one(expanded)

    fused = _fuse([
        _vector_ranking(session, query_vec),
        _lexical_ranking(session, expanded),
    ])
    if not fused:
        return []
    top_ids = fused[:top_k]

    fetch = (
        select(
            RagChunk,
            RagDocument,
            RagChunk.embedding.cosine_distance(query_vec).label("dist"),
        )
        .join(RagDocument, RagChunk.doc_id == RagDocument.id)
        .where(RagChunk.id.in_(top_ids))
    )
    by_id = {
        chunk.id: (chunk, doc, dist)
        for chunk, doc, dist in session.execute(fetch).all()
    }

    result: list[ChatSource] = []
    for cid in top_ids:
        if cid not in by_id:
            continue
        chunk, doc, dist = by_id[cid]
        result.append(
            ChatSource(
                doc_id=doc.id,
                titulo=doc.titulo,
                seccion=_extract_section(chunk.texto),
                chunk_texto=chunk.texto,
                similaridad=round(1.0 - float(dist), 4),
            )
        )
    return result
