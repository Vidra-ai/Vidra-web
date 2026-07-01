"""
Vidra Tracker — cliente para registrar tasks y usage en vidra_api_core.

Soporta contextos síncronos y asíncronos:

    # Async (endpoints async de FastAPI):
    async with tracker.task("radar_priv", metadata={"q": "..."}) as task:
        result = await do_work()
        if task:
            await task.log_usage("anthropic", "claude-sonnet-4-6", 1200, 300, 0.004)

    # Sync (endpoints sync de FastAPI):
    with tracker.task_sync("chatbot", metadata={"q": "..."}) as task:
        result = do_work()

Fallos silenciosos: si vidra_api_core no está disponible, no lanza excepciones.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager, contextmanager
from typing import Any

import httpx

logger = logging.getLogger(__name__)

VIDRA_API_URL = os.getenv("VIDRA_API_URL", "http://vidra_api_core:8000")
VIDRA_API_KEY = os.getenv("VIDRA_API_KEY", "")


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class VidraTask:
    def __init__(self, client: httpx.AsyncClient, task_id: str, api_key: str):
        self._client = client
        self.task_id = task_id
        self._headers = {"X-API-Key": api_key}

    async def log_usage(
        self,
        provider: str,
        model: str,
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        latency_ms: int | None = None,
    ) -> None:
        try:
            payload: dict[str, Any] = {
                "provider": provider, "model": model,
                "tokens_in": tokens_in, "tokens_out": tokens_out, "cost_usd": cost_usd,
            }
            if latency_ms is not None:
                payload["latency_ms"] = latency_ms
            await self._client.post(f"/tasks/{self.task_id}/usage", json=payload,
                                    headers=self._headers, timeout=5)
        except Exception as exc:
            logger.warning("vidra_tracker: log_usage failed: %s", exc)

    async def _set_status(self, status: str, error: str | None = None) -> None:
        try:
            payload: dict[str, Any] = {"status": status}
            if error:
                payload["error"] = error[:500]
            await self._client.patch(f"/tasks/{self.task_id}", json=payload,
                                     headers=self._headers, timeout=5)
        except Exception as exc:
            logger.warning("vidra_tracker: set_status failed: %s", exc)


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class VidraTaskSync:
    def __init__(self, client: httpx.Client, task_id: str, api_key: str):
        self._client = client
        self.task_id = task_id
        self._headers = {"X-API-Key": api_key}

    def log_usage(
        self,
        provider: str,
        model: str,
        tokens_in: int = 0,
        tokens_out: int = 0,
        cost_usd: float = 0.0,
        latency_ms: int | None = None,
    ) -> None:
        try:
            payload: dict[str, Any] = {
                "provider": provider, "model": model,
                "tokens_in": tokens_in, "tokens_out": tokens_out, "cost_usd": cost_usd,
            }
            if latency_ms is not None:
                payload["latency_ms"] = latency_ms
            self._client.post(f"/tasks/{self.task_id}/usage", json=payload,
                              headers=self._headers, timeout=5)
        except Exception as exc:
            logger.warning("vidra_tracker: log_usage failed: %s", exc)

    def _set_status(self, status: str, error: str | None = None) -> None:
        try:
            payload: dict[str, Any] = {"status": status}
            if error:
                payload["error"] = error[:500]
            self._client.patch(f"/tasks/{self.task_id}", json=payload,
                               headers=self._headers, timeout=5)
        except Exception as exc:
            logger.warning("vidra_tracker: set_status failed: %s", exc)


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------

class VidraTracker:
    def __init__(self, base_url: str = VIDRA_API_URL, api_key: str = VIDRA_API_KEY):
        self._base_url = base_url
        self._api_key = api_key

    @asynccontextmanager
    async def task(self, project_slug: str, metadata: dict[str, Any] | None = None):
        task_obj: VidraTask | None = None
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            try:
                resp = await client.post(
                    "/tasks",
                    json={"project_slug": project_slug, "metadata": metadata or {}},
                    headers={"X-API-Key": self._api_key},
                    timeout=5,
                )
                resp.raise_for_status()
                task_obj = VidraTask(client, resp.json()["id"], self._api_key)
                await task_obj._set_status("running")
            except Exception as exc:
                logger.warning("vidra_tracker: could not create task: %s", exc)

            try:
                yield task_obj
                if task_obj:
                    await task_obj._set_status("completed")
            except Exception as exc:
                if task_obj:
                    await task_obj._set_status("failed", error=str(exc))
                raise

    @contextmanager
    def task_sync(self, project_slug: str, metadata: dict[str, Any] | None = None):
        task_obj: VidraTaskSync | None = None
        with httpx.Client(base_url=self._base_url) as client:
            try:
                resp = client.post(
                    "/tasks",
                    json={"project_slug": project_slug, "metadata": metadata or {}},
                    headers={"X-API-Key": self._api_key},
                    timeout=5,
                )
                resp.raise_for_status()
                task_obj = VidraTaskSync(client, resp.json()["id"], self._api_key)
                task_obj._set_status("running")
            except Exception as exc:
                logger.warning("vidra_tracker: could not create task: %s", exc)

            try:
                yield task_obj
                if task_obj:
                    task_obj._set_status("completed")
            except Exception as exc:
                if task_obj:
                    task_obj._set_status("failed", error=str(exc))
                raise
