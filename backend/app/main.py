"""API del Chatbot RAG."""

from __future__ import annotations

import asyncio
import hashlib
import time
from collections import deque
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated
from urllib.parse import urlparse

import httpx
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db, init_db
from app.llm import get_llm_client
from app.models import RagDocument, RagSource
from app.rag.chat import generate_answer
from app.rag.ingest import ingest_document
from app.rag.retriever import retrieve
from app.rag.schemas import (
    ChatRequest,
    ChatResponse,
    DocumentMeta,
    RagSourceIn,
    RagSourceOut,
    SyncResult,
    SyncResultItem,
)
from app.rag.public_docs import sync_public_docs
from app.rag.seed import sync_remote_sources
from app.settings import get_settings

_CHUNK_PREVIEW_LEN = 200
_SYNC_INTERVAL = 24 * 60 * 60


async def _daily_sync_loop() -> None:
    await asyncio.sleep(30)
    while True:
        try:
            await asyncio.to_thread(sync_remote_sources)
        except Exception as exc:
            print(f"[sync] Error en sincronización diaria: {exc}")
        await asyncio.sleep(_SYNC_INTERVAL)


async def _public_docs_sync_loop() -> None:
    """Sincroniza la carpeta pública de Obsidian en bucle corto. Re-embebe solo los
    ficheros cambiados; si no hay cambios, es prácticamente gratis (hash de unos .md)."""
    settings = get_settings()
    if not settings.public_docs_dir.strip():
        print("[public-docs] PUBLIC_DOCS_DIR no configurado: sincronización desactivada.")
        return
    while True:
        try:
            summary = await asyncio.to_thread(sync_public_docs)
            if any(summary[k] for k in ("indexed", "updated", "removed", "errors")):
                print(f"[public-docs] {summary}")
        except Exception as exc:
            print(f"[public-docs] Error en sincronización: {exc}")
        await asyncio.sleep(settings.public_docs_sync_interval)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    init_db()
    tasks = [
        asyncio.create_task(_daily_sync_loop()),
        asyncio.create_task(_public_docs_sync_loop()),
    ]
    yield
    for task in tasks:
        task.cancel()


app = FastAPI(title="Chatbot RAG", version="1.0.0", lifespan=lifespan)

# Rate limiting en memoria por IP para el endpoint público /rag/chat. Evita el abuso
# y el gasto descontrolado en OpenAI. Suficiente para un único contenedor; si se escala
# a varias réplicas, mover el contador a Redis (vidra_redis).
_rate_buckets: dict[str, deque[float]] = {}


def _client_ip(request: Request) -> str:
    """IP real del cliente respetando el proxy inverso (Nginx) vía X-Forwarded-For."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.middleware("http")
async def rate_limit_chat(request: Request, call_next):
    if request.method == "POST" and request.url.path == "/rag/chat":
        settings = get_settings()
        now = time.monotonic()
        window = settings.chat_rate_window
        ip = _client_ip(request)
        bucket = _rate_buckets.setdefault(ip, deque())
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= settings.chat_rate_limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Demasiadas solicitudes. Inténtalo de nuevo en unos segundos."},
            )
        bucket.append(now)
        # Poda defensiva: evita crecimiento ilimitado del diccionario de IPs.
        if len(_rate_buckets) > 10000:
            for k in [k for k, v in _rate_buckets.items() if not v]:
                _rate_buckets.pop(k, None)
    return await call_next(request)


# CORS: orígenes explícitos desde la configuración. No se usa "*" con credenciales
# (combinación que los navegadores rechazan y que abriría la API a cualquier origen).
# Se añade el ÚLTIMO para que sea la capa más externa y añada cabeceras CORS incluso
# a las respuestas 429 que devuelve el rate-limiter.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-Admin-Key"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _require_admin_key(x_admin_key: Annotated[str | None, Header()] = None) -> None:
    settings = get_settings()
    if not settings.admin_api_key:
        raise HTTPException(status_code=404, detail="Not found")
    if x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Forbidden")


@app.post("/rag/documents", response_model=DocumentMeta, status_code=201,
          dependencies=[Depends(_require_admin_key)])
def upload_document(
    session: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    titulo: str = Form(...),
    tipo: str | None = Form(None),
    area: str | None = Form(None),
) -> DocumentMeta:
    content = file.file.read()
    result = ingest_document(session, content, file.filename or titulo, titulo, tipo, area)
    doc = session.get(RagDocument, result.doc_id)
    return DocumentMeta.model_validate(doc)


@app.get("/rag/documents", response_model=list[DocumentMeta],
         dependencies=[Depends(_require_admin_key)])
def list_documents(session: Annotated[Session, Depends(get_db)]) -> list[DocumentMeta]:
    docs = session.execute(select(RagDocument).order_by(RagDocument.created_at.desc())).scalars().all()
    return [DocumentMeta.model_validate(d) for d in docs]


@app.delete("/rag/documents/{doc_id}", status_code=204,
            dependencies=[Depends(_require_admin_key)])
def delete_document(doc_id: int, session: Annotated[Session, Depends(get_db)]) -> None:
    doc = session.get(RagDocument, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    session.delete(doc)
    session.commit()


@app.post("/rag/sources", response_model=RagSourceOut, status_code=201,
          dependencies=[Depends(_require_admin_key)])
def create_source(data: RagSourceIn, session: Annotated[Session, Depends(get_db)]) -> RagSourceOut:
    source = RagSource(url=str(data.url), titulo=data.titulo, tipo=data.tipo, area=data.area)
    session.add(source)
    session.commit()
    session.refresh(source)
    return RagSourceOut.model_validate(source)


@app.get("/rag/sources", response_model=list[RagSourceOut],
         dependencies=[Depends(_require_admin_key)])
def list_sources(session: Annotated[Session, Depends(get_db)]) -> list[RagSourceOut]:
    sources = session.execute(select(RagSource).order_by(RagSource.created_at.desc())).scalars().all()
    return [RagSourceOut.model_validate(s) for s in sources]


@app.delete("/rag/sources/{source_id}", status_code=204,
            dependencies=[Depends(_require_admin_key)])
def delete_source(source_id: int, session: Annotated[Session, Depends(get_db)]) -> None:
    source = session.get(RagSource, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Fuente no encontrada")
    if source.doc_id:
        doc = session.get(RagDocument, source.doc_id)
        if doc:
            session.delete(doc)
    session.delete(source)
    session.commit()


@app.post("/rag/sync", response_model=SyncResult,
          dependencies=[Depends(_require_admin_key)])
def sync_sources(session: Annotated[Session, Depends(get_db)]) -> SyncResult:
    sources = session.execute(
        select(RagSource).where(RagSource.enabled == True)  # noqa: E712
    ).scalars().all()

    items: list[SyncResultItem] = []
    for source in sources:
        try:
            response = httpx.get(str(source.url), follow_redirects=True, timeout=30.0)
            response.raise_for_status()
            content = response.content
            new_hash = hashlib.sha256(content).hexdigest()

            if new_hash == source.content_hash:
                items.append(SyncResultItem(source_id=source.id, url=source.url, status="unchanged"))
                continue

            if source.doc_id:
                old_doc = session.get(RagDocument, source.doc_id)
                if old_doc:
                    session.delete(old_doc)
                    session.flush()

            path = urlparse(str(source.url)).path
            filename = path.rstrip("/").split("/")[-1] or "documento"
            result = ingest_document(session, content, filename, source.titulo, source.tipo, source.area)

            source.content_hash = new_hash
            source.doc_id = result.doc_id
            source.last_synced_at = datetime.now(timezone.utc)
            session.commit()

            items.append(SyncResultItem(
                source_id=source.id, url=source.url, status="updated",
                detail=f"{result.chunks} chunks indexados"
            ))
        except Exception as exc:
            session.rollback()
            items.append(SyncResultItem(source_id=source.id, url=source.url, status="error", detail=str(exc)))

    return SyncResult(
        synced=sum(1 for i in items if i.status == "updated"),
        unchanged=sum(1 for i in items if i.status == "unchanged"),
        errors=sum(1 for i in items if i.status == "error"),
        items=items,
    )


@app.post("/rag/sync-public", dependencies=[Depends(_require_admin_key)])
def sync_public(_session: Annotated[Session, Depends(get_db)]) -> dict:
    """Fuerza una sincronización inmediata de la carpeta pública de Obsidian."""
    return sync_public_docs()


@app.post("/rag/chat", response_model=ChatResponse)
def rag_chat(req: ChatRequest, session: Annotated[Session, Depends(get_db)]) -> ChatResponse:
    client = get_llm_client(get_settings())

    retrieval_query = req.pregunta
    if req.historial:
        prev_user = [m.contenido for m in req.historial if m.rol == "usuario"][-2:]
        if prev_user:
            retrieval_query = " ".join(prev_user) + " " + req.pregunta

    fuentes = retrieve(session, retrieval_query, req.top_k)
    result = generate_answer(req.pregunta, fuentes, client, req.historial)

    for f in result.fuentes:
        if len(f.chunk_texto) > _CHUNK_PREVIEW_LEN:
            f.chunk_texto = f.chunk_texto[:_CHUNK_PREVIEW_LEN] + "…"
    return result
