"""Tests de integración para headers de seguridad y política CORS."""

import httpx
import pytest

CHAT_URL = "/rag/chat"
VALID_QUESTION = "¿Qué servicios ofrece Vidra?"


# ---------------------------------------------------------------------------
# Headers de seguridad (verificados en /health para evitar coste de LLM)
# ---------------------------------------------------------------------------

class TestSecurityHeaders:
    """Verifica la presencia y valor correcto de los headers de seguridad HTTP."""

    def test_hsts_header_present(self, client: httpx.Client) -> None:
        """Strict-Transport-Security debe estar presente."""
        response = client.get("/health")
        assert "strict-transport-security" in response.headers

    def test_hsts_max_age_at_least_one_year(self, client: httpx.Client) -> None:
        """HSTS max-age debe ser al menos 31536000 (1 año)."""
        hsts = client.get("/health").headers.get("strict-transport-security", "")
        # Extraer el valor de max-age
        for part in hsts.split(";"):
            part = part.strip()
            if part.lower().startswith("max-age="):
                max_age = int(part.split("=", 1)[1].strip())
                assert max_age >= 31536000, f"HSTS max-age demasiado bajo: {max_age}"
                return
        pytest.fail(f"max-age no encontrado en HSTS header: '{hsts}'")

    def test_hsts_includes_subdomains(self, client: httpx.Client) -> None:
        """HSTS debe incluir includeSubDomains."""
        hsts = client.get("/health").headers.get("strict-transport-security", "")
        assert "includeSubDomains" in hsts, f"includeSubDomains no encontrado en: '{hsts}'"

    def test_x_frame_options_is_deny(self, client: httpx.Client) -> None:
        """X-Frame-Options debe ser DENY."""
        response = client.get("/health")
        x_frame = response.headers.get("x-frame-options", "")
        assert x_frame.upper() == "DENY", f"X-Frame-Options inesperado: '{x_frame}'"

    def test_x_content_type_options_is_nosniff(self, client: httpx.Client) -> None:
        """X-Content-Type-Options debe ser nosniff."""
        response = client.get("/health")
        x_cto = response.headers.get("x-content-type-options", "")
        assert x_cto.lower() == "nosniff", f"X-Content-Type-Options inesperado: '{x_cto}'"

    def test_referrer_policy_present(self, client: httpx.Client) -> None:
        """Referrer-Policy debe estar presente."""
        response = client.get("/health")
        assert "referrer-policy" in response.headers

    def test_referrer_policy_is_strict_origin_when_cross_origin(self, client: httpx.Client) -> None:
        """Referrer-Policy debe ser strict-origin-when-cross-origin."""
        referrer = client.get("/health").headers.get("referrer-policy", "")
        assert referrer.lower() == "strict-origin-when-cross-origin", (
            f"Referrer-Policy inesperado: '{referrer}'"
        )

    def test_server_header_does_not_expose_uvicorn(self, client: httpx.Client) -> None:
        """El header Server no debe revelar 'uvicorn' (fingerprinting del servidor)."""
        server = client.get("/health").headers.get("server", "")
        assert "uvicorn" not in server.lower(), (
            f"El header Server expone el servidor interno: '{server}'"
        )

    def test_server_header_is_vidra_or_nginx(self, client: httpx.Client) -> None:
        """El header Server debe ser 'vidra' o 'nginx', no el valor por defecto de uvicorn."""
        server = client.get("/health").headers.get("server", "").lower()
        assert server in ("vidra", "nginx"), (
            f"Server header inesperado: '{server}' (se esperaba 'vidra' o 'nginx')"
        )

    def test_security_headers_present_on_chat_endpoint(self, client: httpx.Client) -> None:
        """Los headers de seguridad también deben estar presentes en respuestas del endpoint /rag/chat."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION})
        assert "x-frame-options" in response.headers
        assert "x-content-type-options" in response.headers
        assert "strict-transport-security" in response.headers

    def test_security_headers_present_on_403_response(self, client: httpx.Client) -> None:
        """Los headers de seguridad deben estar presentes incluso en respuestas 403."""
        response = client.get("/rag/documents")
        assert response.status_code == 403
        assert "x-frame-options" in response.headers
        assert "x-content-type-options" in response.headers


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

class TestCorsPolicy:
    """Verifica la política CORS: origen permitido y origen denegado."""

    def test_cors_allowed_for_vidra_origin(self, client: httpx.Client) -> None:
        """El origen https://vidra-ia.com debe recibir el header Access-Control-Allow-Origin."""
        response = client.options(
            CHAT_URL,
            headers={
                "Origin": "https://vidra-ia.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        acao = response.headers.get("access-control-allow-origin", "")
        assert acao == "https://vidra-ia.com", (
            f"CORS no habilitado para origen legítimo. access-control-allow-origin: '{acao}'"
        )

    def test_cors_get_health_with_vidra_origin(self, client: httpx.Client) -> None:
        """GET /health con Origin vidra-ia.com debe devolver access-control-allow-origin."""
        response = client.get("/health", headers={"Origin": "https://vidra-ia.com"})
        acao = response.headers.get("access-control-allow-origin", "")
        assert acao == "https://vidra-ia.com"

    def test_cors_blocked_for_evil_origin(self, client: httpx.Client) -> None:
        """El origen https://evil.com NO debe aparecer en Access-Control-Allow-Origin."""
        response = client.options(
            CHAT_URL,
            headers={
                "Origin": "https://evil.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        acao = response.headers.get("access-control-allow-origin", "")
        assert acao != "https://evil.com", (
            "El origen evil.com no debería estar permitido por CORS"
        )
        assert acao != "*", (
            "access-control-allow-origin no debe ser '*' (wildcard) cuando evil.com hace la petición"
        )

    def test_cors_evil_origin_not_reflected(self, client: httpx.Client) -> None:
        """El servidor no debe reflejar (echo) el origen de evil.com en la respuesta."""
        response = client.get("/health", headers={"Origin": "https://evil.com"})
        acao = response.headers.get("access-control-allow-origin", "")
        assert "evil.com" not in acao

    def test_cors_no_wildcard_on_legitimate_request(self, client: httpx.Client) -> None:
        """CORS no debe usar '*' (wildcard); debe especificar el origen exacto."""
        response = client.get("/health", headers={"Origin": "https://vidra-ia.com"})
        acao = response.headers.get("access-control-allow-origin", "")
        assert acao != "*", (
            "CORS no debe usar '*'; debe retornar el origen exacto para compatibilidad con credenciales"
        )
