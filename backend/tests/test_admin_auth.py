"""Tests de integración para la autenticación de endpoints admin y rutas desactivadas."""

import httpx
import pytest


# ---------------------------------------------------------------------------
# Endpoints admin que requieren x-admin-key
# ---------------------------------------------------------------------------

class TestAdminAuth:
    """Verifica que todos los endpoints protegidos devuelven 403 sin credenciales válidas."""

    # --- GET /rag/documents ---

    def test_get_documents_without_key_returns_403(self, client: httpx.Client) -> None:
        """GET /rag/documents sin header debe devolver 403."""
        response = client.get("/rag/documents")
        assert response.status_code == 403

    def test_get_documents_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """GET /rag/documents con x-admin-key vacío debe devolver 403."""
        response = client.get("/rag/documents", headers={"x-admin-key": ""})
        assert response.status_code == 403

    def test_get_documents_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """GET /rag/documents con x-admin-key incorrecto debe devolver 403."""
        response = client.get("/rag/documents", headers={"x-admin-key": "wrong"})
        assert response.status_code == 403

    # --- POST /rag/documents ---

    def test_post_documents_without_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/documents sin header debe devolver 403."""
        response = client.post("/rag/documents", data={"titulo": "test"})
        assert response.status_code == 403

    def test_post_documents_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/documents con x-admin-key vacío debe devolver 403."""
        response = client.post(
            "/rag/documents",
            data={"titulo": "test"},
            headers={"x-admin-key": ""},
        )
        assert response.status_code == 403

    def test_post_documents_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/documents con x-admin-key incorrecto debe devolver 403."""
        response = client.post(
            "/rag/documents",
            data={"titulo": "test"},
            headers={"x-admin-key": "wrong"},
        )
        assert response.status_code == 403

    # --- GET /rag/sources ---

    def test_get_sources_without_key_returns_403(self, client: httpx.Client) -> None:
        """GET /rag/sources sin header debe devolver 403."""
        response = client.get("/rag/sources")
        assert response.status_code == 403

    def test_get_sources_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """GET /rag/sources con x-admin-key vacío debe devolver 403."""
        response = client.get("/rag/sources", headers={"x-admin-key": ""})
        assert response.status_code == 403

    def test_get_sources_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """GET /rag/sources con x-admin-key incorrecto debe devolver 403."""
        response = client.get("/rag/sources", headers={"x-admin-key": "wrong"})
        assert response.status_code == 403

    # --- POST /rag/sources ---

    def test_post_sources_without_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sources sin header debe devolver 403."""
        response = client.post(
            "/rag/sources",
            json={"url": "https://example.com", "titulo": "test"},
        )
        assert response.status_code == 403

    def test_post_sources_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sources con x-admin-key vacío debe devolver 403."""
        response = client.post(
            "/rag/sources",
            json={"url": "https://example.com", "titulo": "test"},
            headers={"x-admin-key": ""},
        )
        assert response.status_code == 403

    def test_post_sources_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sources con x-admin-key incorrecto debe devolver 403."""
        response = client.post(
            "/rag/sources",
            json={"url": "https://example.com", "titulo": "test"},
            headers={"x-admin-key": "wrong"},
        )
        assert response.status_code == 403

    # --- POST /rag/sync ---

    def test_post_sync_without_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sync sin header debe devolver 403."""
        response = client.post("/rag/sync")
        assert response.status_code == 403

    def test_post_sync_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sync con x-admin-key vacío debe devolver 403."""
        response = client.post("/rag/sync", headers={"x-admin-key": ""})
        assert response.status_code == 403

    def test_post_sync_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sync con x-admin-key incorrecto debe devolver 403."""
        response = client.post("/rag/sync", headers={"x-admin-key": "wrong"})
        assert response.status_code == 403

    # --- POST /rag/sync-public ---

    def test_post_sync_public_without_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sync-public sin header debe devolver 403."""
        response = client.post("/rag/sync-public")
        assert response.status_code == 403

    def test_post_sync_public_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sync-public con x-admin-key vacío debe devolver 403."""
        response = client.post("/rag/sync-public", headers={"x-admin-key": ""})
        assert response.status_code == 403

    def test_post_sync_public_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """POST /rag/sync-public con x-admin-key incorrecto debe devolver 403."""
        response = client.post("/rag/sync-public", headers={"x-admin-key": "wrong"})
        assert response.status_code == 403

    # --- DELETE /rag/documents/{id} ---

    def test_delete_document_without_key_returns_403(self, client: httpx.Client) -> None:
        """DELETE /rag/documents/1 sin header debe devolver 403."""
        response = client.delete("/rag/documents/1")
        assert response.status_code == 403

    def test_delete_document_with_empty_key_returns_403(self, client: httpx.Client) -> None:
        """DELETE /rag/documents/1 con x-admin-key vacío debe devolver 403."""
        response = client.delete("/rag/documents/1", headers={"x-admin-key": ""})
        assert response.status_code == 403

    def test_delete_document_with_wrong_key_returns_403(self, client: httpx.Client) -> None:
        """DELETE /rag/documents/1 con x-admin-key incorrecto debe devolver 403."""
        response = client.delete("/rag/documents/1", headers={"x-admin-key": "wrong"})
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Rutas de documentación desactivadas en producción
# ---------------------------------------------------------------------------

class TestDocsDisabled:
    """Verifica que las rutas de documentación están desactivadas en producción."""

    def test_docs_endpoint_returns_404(self, client: httpx.Client) -> None:
        """GET /docs debe devolver 404 (documentación desactivada en producción)."""
        response = client.get("/docs")
        assert response.status_code == 404

    def test_openapi_json_returns_404(self, client: httpx.Client) -> None:
        """GET /openapi.json debe devolver 404."""
        response = client.get("/openapi.json")
        assert response.status_code == 404

    def test_redoc_returns_404(self, client: httpx.Client) -> None:
        """GET /redoc debe devolver 404."""
        response = client.get("/redoc")
        assert response.status_code == 404
