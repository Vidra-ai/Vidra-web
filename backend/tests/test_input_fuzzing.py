"""Tests de fuzzing de input contra POST /rag/chat.

El objetivo es verificar que la API devuelve 200 o 422 ante cualquier entrada
maliciosa, y NUNCA 500. Tampoco debe ejecutar los payloads como código ni
filtrar contenido del sistema de ficheros del servidor.

Categorías cubiertas:
- XSS
- SSTI (Server-Side Template Injection)
- Path traversal
- Command injection
- CRLF injection
- Null bytes y caracteres de control
- JSON injection (campos extra, tipos incorrectos)
"""

import httpx
import pytest

CHAT_URL = "/rag/chat"


# ---------------------------------------------------------------------------
# XSS
# ---------------------------------------------------------------------------

XSS_PAYLOADS = [
    ("script_tag", "<script>alert(1)</script>"),
    ("img_onerror", "<img src=x onerror=alert(1)>"),
    ("javascript_proto", "javascript:alert(1)"),
    ("quote_script", '"><script>alert(1)</script>'),
    ("onmouseover", "' onmouseover='alert(1)"),
    ("svg_onload", "<svg onload=alert(1)>"),
]


class TestXSSPayloads:
    """Los payloads XSS deben devolver 200 o 422; nunca 500."""

    @pytest.mark.parametrize("name,payload", XSS_PAYLOADS, ids=[p[0] for p in XSS_PAYLOADS])
    def test_xss_payload_does_not_cause_500(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Un payload XSS como pregunta nunca debe provocar un error 500."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code in (200, 422), (
            f"Payload XSS '{name}' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )

    @pytest.mark.parametrize("name,payload", XSS_PAYLOADS, ids=[p[0] for p in XSS_PAYLOADS])
    def test_xss_payload_200_response_is_plain_string(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Si el endpoint devuelve 200, el campo 'respuesta' debe ser un string plano."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        if response.status_code != 200:
            pytest.skip(f"Payload '{name}' devolvió {response.status_code}; no aplica")
        body = response.json()
        assert isinstance(body.get("respuesta"), str), (
            f"El campo 'respuesta' no es un string para payload '{name}'"
        )


# ---------------------------------------------------------------------------
# SSTI (Server-Side Template Injection)
# ---------------------------------------------------------------------------

SSTI_PAYLOADS = [
    ("jinja2_multiply", "{{7*7}}"),
    ("dollar_multiply", "${7*7}"),
    ("erb_multiply", "<%= 7*7 %>"),
    ("ruby_multiply", "#{7*7}"),
    ("jinja2_config", "{{config}}"),
    ("jinja2_mro", "{{''.__class__.__mro__}}"),
]


class TestSSTIPayloads:
    """Los payloads SSTI no deben provocar 500 ni ejecutar expresiones en el servidor."""

    @pytest.mark.parametrize("name,payload", SSTI_PAYLOADS, ids=[p[0] for p in SSTI_PAYLOADS])
    def test_ssti_payload_does_not_cause_500(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Un payload SSTI nunca debe provocar un error 500."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code in (200, 422), (
            f"Payload SSTI '{name}' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )

    @pytest.mark.parametrize("name,payload", SSTI_PAYLOADS, ids=[p[0] for p in SSTI_PAYLOADS])
    def test_ssti_payload_does_not_evaluate_expression(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Si el endpoint devuelve 200, la respuesta no debe contener '49' aislado (7*7 evaluado)."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        if response.status_code != 200:
            pytest.skip(f"Payload '{name}' devolvió {response.status_code}; no aplica")
        body = response.json()
        respuesta = body.get("respuesta", "")
        # Buscar "49" como número aislado: indicaría que la expresión {{7*7}} se evaluó
        import re
        assert not re.search(r"\b49\b", respuesta), (
            f"La respuesta contiene '49' para el payload SSTI '{name}', "
            f"lo que podría indicar ejecución de plantilla: {respuesta[:200]}"
        )


# ---------------------------------------------------------------------------
# Path traversal
# ---------------------------------------------------------------------------

PATH_TRAVERSAL_PAYLOADS = [
    ("dotdot_unix", "../../../etc/passwd"),
    ("dotdot_urlencoded", "..%2F..%2F..%2Fetc%2Fpasswd"),
    ("absolute_passwd", "/etc/passwd"),
    ("dotdot_shadow", "../../../../etc/shadow"),
]

PASSWD_INDICATORS = ["root:x:", "nobody:"]


class TestPathTraversalPayloads:
    """Los payloads de path traversal no deben provocar 500 ni filtrar contenido del sistema."""

    @pytest.mark.parametrize(
        "name,payload", PATH_TRAVERSAL_PAYLOADS, ids=[p[0] for p in PATH_TRAVERSAL_PAYLOADS]
    )
    def test_path_traversal_does_not_cause_500(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Un payload de path traversal nunca debe provocar un error 500."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code in (200, 422), (
            f"Payload '{name}' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )

    @pytest.mark.parametrize(
        "name,payload", PATH_TRAVERSAL_PAYLOADS, ids=[p[0] for p in PATH_TRAVERSAL_PAYLOADS]
    )
    def test_path_traversal_does_not_leak_passwd(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Si devuelve 200, la respuesta no debe contener contenido de /etc/passwd."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        if response.status_code != 200:
            pytest.skip(f"Payload '{name}' devolvió {response.status_code}; no aplica")
        body_text = response.text
        for indicator in PASSWD_INDICATORS:
            assert indicator not in body_text, (
                f"Payload '{name}': la respuesta contiene '{indicator}', "
                f"posible filtración de /etc/passwd."
            )


# ---------------------------------------------------------------------------
# Command injection
# ---------------------------------------------------------------------------

CMDI_PAYLOADS = [
    ("semicolon_ls", "; ls -la"),
    ("pipe_cat_passwd", "| cat /etc/passwd"),
    ("and_whoami", "&& whoami"),
    ("subshell_id", "$(id)"),
    ("backtick_id", "`id`"),
    ("ping_evil", "; ping -c 1 evil.com"),
]

COMMAND_OUTPUT_INDICATORS = ["uid=", "root:", "drwxr-xr-x"]


class TestCommandInjectionPayloads:
    """Los payloads de command injection no deben provocar 500 ni filtrar salida de comandos."""

    @pytest.mark.parametrize("name,payload", CMDI_PAYLOADS, ids=[p[0] for p in CMDI_PAYLOADS])
    def test_cmdi_payload_does_not_cause_500(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Un payload de command injection nunca debe provocar un error 500."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code in (200, 422), (
            f"Payload '{name}' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )

    @pytest.mark.parametrize("name,payload", CMDI_PAYLOADS, ids=[p[0] for p in CMDI_PAYLOADS])
    def test_cmdi_payload_does_not_leak_command_output(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Si devuelve 200, la respuesta no debe contener salida típica de comandos de shell."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        if response.status_code != 200:
            pytest.skip(f"Payload '{name}' devolvió {response.status_code}; no aplica")
        body_text = response.text
        for indicator in COMMAND_OUTPUT_INDICATORS:
            assert indicator not in body_text, (
                f"Payload '{name}': la respuesta contiene '{indicator}', "
                f"posible ejecución de comando en el servidor."
            )


# ---------------------------------------------------------------------------
# CRLF injection
# ---------------------------------------------------------------------------

CRLF_PAYLOADS = [
    ("crlf_set_cookie", "test\r\nSet-Cookie: session=hacked"),
    ("crlf_script_inject", "test\r\n\r\n<script>alert(1)</script>"),
]


class TestCRLFInjectionPayloads:
    """Los payloads CRLF no deben provocar 500 ni inyectar headers en la respuesta."""

    @pytest.mark.parametrize("name,payload", CRLF_PAYLOADS, ids=[p[0] for p in CRLF_PAYLOADS])
    def test_crlf_payload_does_not_cause_500(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Un payload CRLF nunca debe provocar un error 500."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code in (200, 422), (
            f"Payload CRLF '{name}' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )

    @pytest.mark.parametrize("name,payload", CRLF_PAYLOADS, ids=[p[0] for p in CRLF_PAYLOADS])
    def test_crlf_does_not_inject_cookie_header(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Los headers de respuesta no deben contener 'session=hacked' inyectado por CRLF."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        combined_headers = " ".join(
            f"{k}: {v}" for k, v in response.headers.items()
        ).lower()
        assert "session=hacked" not in combined_headers, (
            f"Payload CRLF '{name}' inyectó 'session=hacked' en los headers de respuesta."
        )


# ---------------------------------------------------------------------------
# Null bytes y caracteres de control
# ---------------------------------------------------------------------------

NULL_BYTE_PAYLOADS = [
    ("null_byte_mid", "pregunta\x00maliciosa"),
    ("null_bytes_triple", "test\x00\x00\x00"),
]


class TestNullBytePayloads:
    """Los payloads con null bytes no deben provocar 500."""

    @pytest.mark.parametrize(
        "name,payload", NULL_BYTE_PAYLOADS, ids=[p[0] for p in NULL_BYTE_PAYLOADS]
    )
    def test_null_byte_payload_does_not_cause_500(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Un payload con null bytes nunca debe provocar un error 500."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code in (200, 422), (
            f"Payload '{name}' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )


# ---------------------------------------------------------------------------
# JSON injection
# ---------------------------------------------------------------------------

class TestJSONInjectionPayloads:
    """Los payloads de JSON injection deben ser rechazados con 422."""

    def test_extra_proto_field_does_not_cause_500(self, client: httpx.Client) -> None:
        """Un body con '__proto__' extra no debe causar un error 500. FastAPI/Pydantic ignora
        los campos desconocidos (devuelve 200) o los rechaza (422); ambos son aceptables."""
        response = client.post(
            CHAT_URL,
            json={"pregunta": "test", "__proto__": {"isAdmin": True}},
        )
        assert response.status_code in (200, 422), (
            f"Body con '__proto__' devolvió {response.status_code} (esperado 200 o 422).\n"
            f"Body: {response.text[:300]}"
        )

    def test_pregunta_as_integer_returns_422(self, client: httpx.Client) -> None:
        """Un body donde 'pregunta' es un entero debe ser rechazado con 422."""
        response = client.post(CHAT_URL, json={"pregunta": 12345})
        assert response.status_code == 422, (
            f"Body con pregunta=12345 (entero) devolvió {response.status_code} (esperado 422).\n"
            f"Body: {response.text[:300]}"
        )
