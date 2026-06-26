"""Tests de integración para el rate limiting de POST /rag/chat.

ADVERTENCIA: Estos tests modifican el estado del servidor (buckets de sliding
window en Redis o memoria). Necesitan al menos 60 segundos de separación entre
ejecuciones sobre el mismo rango IP para que el bucket expire y los tests no
interfieran entre sí.

Implementación del rate limit en producción:
- Sliding window: 20 req/min + 100/día por IP
- La IP se extrae del PRIMER elemento del header X-Forwarded-For

Estos tests usan el rango 192.0.2.x (TEST-NET-1, RFC 5737) para no contaminar
los buckets de IPs reales.
"""

import httpx
import pytest

CHAT_URL = "/rag/chat"

# Cuerpo intencionalmente inválido: pregunta vacía → 422 sin llamada al LLM.
# Usamos esto para consumir el rate limit rápidamente sin coste de inferencia.
INVALID_BODY = {"pregunta": ""}

pytestmark = pytest.mark.slow


class TestRateLimit:
    """Verifica el comportamiento del rate limiting a nivel de IP."""

    def test_rate_limit_triggers_after_20_requests(self, client: httpx.Client) -> None:
        """Las primeras 20 peticiones deben devolver 422; la 21ª debe devolver 429."""
        ip = "192.0.2.100"
        headers = {"X-Forwarded-For": ip}

        # Las primeras 20 peticiones deben ser aceptadas por el rate limiter
        # (aunque fallen con 422 por validación de input)
        for i in range(1, 21):
            response = client.post(CHAT_URL, json=INVALID_BODY, headers=headers)
            assert response.status_code == 422, (
                f"Petición {i}/20: se esperaba 422, se obtuvo {response.status_code}. "
                f"El rate limit se disparó antes del límite (IP: {ip})."
            )

        # La petición 21 debe ser bloqueada por el rate limiter
        response = client.post(CHAT_URL, json=INVALID_BODY, headers=headers)
        assert response.status_code == 429, (
            f"Petición 21: se esperaba 429 (rate limit), se obtuvo {response.status_code}. "
            f"El rate limit no se está aplicando correctamente (IP: {ip})."
        )

    def test_rate_limit_response_has_retry_after_header(self, client: httpx.Client) -> None:
        """La respuesta 429 debe incluir el header 'retry-after' con un valor numérico > 0."""
        ip = "192.0.2.101"
        headers = {"X-Forwarded-For": ip}

        # Consumir las 20 peticiones del bucket
        for _ in range(20):
            client.post(CHAT_URL, json=INVALID_BODY, headers=headers)

        # La 21ª debe devolver 429 con retry-after
        response = client.post(CHAT_URL, json=INVALID_BODY, headers=headers)
        assert response.status_code == 429, (
            f"Se esperaba 429 en la petición 21 (IP: {ip}), "
            f"se obtuvo {response.status_code}."
        )

        retry_after = response.headers.get("retry-after")
        assert retry_after is not None, (
            "La respuesta 429 no incluye el header 'retry-after'."
        )
        assert retry_after.strip().isdigit(), (
            f"El header 'retry-after' no es un entero: '{retry_after}'."
        )
        assert int(retry_after) > 0, (
            f"El header 'retry-after' debe ser > 0, se obtuvo: {retry_after}."
        )

    def test_rate_limit_body_has_detail_field(self, client: httpx.Client) -> None:
        """El cuerpo de la respuesta 429 debe contener el campo 'detail' con texto."""
        ip = "192.0.2.102"
        headers = {"X-Forwarded-For": ip}

        for _ in range(20):
            client.post(CHAT_URL, json=INVALID_BODY, headers=headers)

        response = client.post(CHAT_URL, json=INVALID_BODY, headers=headers)
        assert response.status_code == 429, (
            f"Se esperaba 429 en la petición 21 (IP: {ip}), "
            f"se obtuvo {response.status_code}."
        )

        body = response.json()
        assert "detail" in body, (
            f"La respuesta 429 no contiene el campo 'detail'. Body: {body}"
        )
        assert isinstance(body["detail"], str) and len(body["detail"]) > 0, (
            f"El campo 'detail' está vacío o no es un string. Body: {body}"
        )

    def test_rate_limit_different_ips_are_independent(self, client: httpx.Client) -> None:
        """Los buckets de rate limit son independientes por IP."""
        ip_a = "192.0.2.110"
        ip_b = "192.0.2.111"

        # Consumir el bucket completo de ip_a (20 peticiones)
        for i in range(1, 21):
            response = client.post(
                CHAT_URL, json=INVALID_BODY, headers={"X-Forwarded-For": ip_a}
            )
            assert response.status_code == 422, (
                f"IP A, petición {i}/20: se esperaba 422, "
                f"se obtuvo {response.status_code}."
            )

        # ip_b no ha consumido nada; su primera petición debe pasar el rate limiter
        response = client.post(
            CHAT_URL, json=INVALID_BODY, headers={"X-Forwarded-For": ip_b}
        )
        assert response.status_code == 422, (
            f"IP B primera petición: se esperaba 422 (bucket independiente), "
            f"se obtuvo {response.status_code}. El rate limit de ip_a contaminó el de ip_b."
        )

    def test_rate_limit_xforwardedfor_spoofing_bypasses_limit(
        self, client: httpx.Client
    ) -> None:
        """
        [VULNERABILITY DEMO] Rotando la IP en X-Forwarded-For se evita el rate limit.

        # VID-013: X-Forwarded-For spoofing bypasses rate limiting.
        #   Fix: use --forwarded-allow-ips=127.0.0.1 in uvicorn so only nginx's
        #   real client IP is trusted, not client-controlled headers.
        """
        # Enviamos 25 peticiones rotando entre 5 IPs ficticias (192.0.2.200-204).
        # Cada bucket solo recibe 5 peticiones, muy por debajo del límite de 20.
        # Si el rate limit toma el X-Forwarded-For sin validación, ninguna
        # petición debe devolver 429.
        for i in range(25):
            spoofed_ip = f"192.0.2.{200 + (i % 5)}"
            response = client.post(
                CHAT_URL,
                json=INVALID_BODY,
                headers={"X-Forwarded-For": spoofed_ip},
            )
            assert response.status_code != 429, (
                f"Petición {i + 1} con IP rotada '{spoofed_ip}' devolvió 429. "
                f"El spoofing debería haber evitado el rate limit (esta es la vulnerabilidad)."
            )
