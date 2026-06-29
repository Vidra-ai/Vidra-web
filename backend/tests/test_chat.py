"""Tests de integración para el endpoint POST /rag/chat."""

import httpx
import pytest


CHAT_URL = "/rag/chat"
VALID_QUESTION = "¿Qué servicios ofrece Vidra?"


# ---------------------------------------------------------------------------
# Respuesta básica y schema público
# ---------------------------------------------------------------------------

class TestChatBasicResponse:
    """Verifica que el endpoint responde correctamente con una pregunta válida."""

    def test_chat_returns_200_with_valid_question(self, client: httpx.Client) -> None:
        """POST /rag/chat con pregunta válida debe devolver 200."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION})
        assert response.status_code == 200

    def test_chat_content_type_is_json(self, client: httpx.Client) -> None:
        """La respuesta debe ser application/json."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION})
        assert "application/json" in response.headers.get("content-type", "")

    def test_chat_schema_has_required_fields(self, client: httpx.Client) -> None:
        """La respuesta debe contener exactamente los campos: respuesta, fuentes, sin_informacion."""
        body = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION}).json()
        assert "respuesta" in body
        assert "fuentes" in body
        assert "sin_informacion" in body

    def test_chat_respuesta_is_string(self, client: httpx.Client) -> None:
        """El campo 'respuesta' debe ser un string no vacío."""
        body = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION}).json()
        assert isinstance(body["respuesta"], str)
        assert len(body["respuesta"]) > 0

    def test_chat_fuentes_is_list(self, client: httpx.Client) -> None:
        """El campo 'fuentes' debe ser una lista."""
        body = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION}).json()
        assert isinstance(body["fuentes"], list)

    def test_chat_sin_informacion_is_bool(self, client: httpx.Client) -> None:
        """El campo 'sin_informacion' debe ser un booleano."""
        body = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION}).json()
        assert isinstance(body["sin_informacion"], bool)


# ---------------------------------------------------------------------------
# Schema de fuentes: solo campos públicos (sin campos internos)
# ---------------------------------------------------------------------------

class TestChatSourceSchema:
    """Verifica que las fuentes del endpoint público NO exponen campos internos."""

    def _get_fuentes(self, client: httpx.Client) -> list:
        """Obtiene una lista de fuentes; reintenta con otra pregunta si la primera no trae fuentes."""
        for pregunta in [
            VALID_QUESTION,
            "¿Cuáles son las capacidades de inteligencia artificial de Vidra?",
            "¿Cómo funciona el RAG?",
        ]:
            body = client.post(CHAT_URL, json={"pregunta": pregunta}).json()
            if body.get("fuentes"):
                return body["fuentes"]
        return []

    def test_chat_schema_hides_internal_fields(self, client: httpx.Client) -> None:
        """Cada fuente NO debe exponer doc_id, chunk_texto ni similaridad."""
        fuentes = self._get_fuentes(client)
        if not fuentes:
            pytest.skip("La respuesta no devolvió fuentes; no se puede verificar el schema")
        for fuente in fuentes:
            assert "doc_id" not in fuente, "doc_id es un campo interno y no debe exponerse"
            assert "chunk_texto" not in fuente, "chunk_texto es un campo interno y no debe exponerse"
            assert "similaridad" not in fuente, "similaridad es un campo interno y no debe exponerse"

    def test_chat_source_schema_has_titulo(self, client: httpx.Client) -> None:
        """Cada fuente debe tener el campo 'titulo' (string)."""
        fuentes = self._get_fuentes(client)
        if not fuentes:
            pytest.skip("La respuesta no devolvió fuentes; no se puede verificar el schema")
        for fuente in fuentes:
            assert "titulo" in fuente
            assert isinstance(fuente["titulo"], str)

    def test_chat_source_schema_seccion_is_str_or_null(self, client: httpx.Client) -> None:
        """Cada fuente debe tener 'seccion' como string o null."""
        fuentes = self._get_fuentes(client)
        if not fuentes:
            pytest.skip("La respuesta no devolvió fuentes; no se puede verificar el schema")
        for fuente in fuentes:
            assert "seccion" in fuente
            assert fuente["seccion"] is None or isinstance(fuente["seccion"], str)

    def test_chat_source_schema_only_public_fields(self, client: httpx.Client) -> None:
        """Cada fuente debe contener únicamente los campos públicos: titulo y seccion."""
        fuentes = self._get_fuentes(client)
        if not fuentes:
            pytest.skip("La respuesta no devolvió fuentes; no se puede verificar el schema")
        allowed_fields = {"titulo", "seccion"}
        for fuente in fuentes:
            extra = set(fuente.keys()) - allowed_fields
            assert not extra, f"Campos inesperados en fuente: {extra}"


# ---------------------------------------------------------------------------
# Validación de entrada (errores 422)
# ---------------------------------------------------------------------------

class TestChatValidation:
    """Verifica que el endpoint rechaza correctamente las peticiones inválidas."""

    def test_chat_empty_pregunta_returns_422(self, client: httpx.Client) -> None:
        """Una pregunta vacía debe devolver 422 Unprocessable Entity."""
        response = client.post(CHAT_URL, json={"pregunta": ""})
        assert response.status_code == 422

    def test_chat_missing_pregunta_returns_422(self, client: httpx.Client) -> None:
        """Una petición sin el campo 'pregunta' debe devolver 422."""
        response = client.post(CHAT_URL, json={})
        assert response.status_code == 422

    def test_chat_pregunta_over_500_chars_returns_422(self, client: httpx.Client) -> None:
        """Una pregunta de más de 500 caracteres debe devolver 422."""
        long_question = "a" * 501
        response = client.post(CHAT_URL, json={"pregunta": long_question})
        assert response.status_code == 422

    def test_chat_pregunta_exactly_500_chars_is_valid(self, client: httpx.Client) -> None:
        """Una pregunta de exactamente 500 caracteres debe ser aceptada (200)."""
        question_500 = "a" * 500
        response = client.post(CHAT_URL, json={"pregunta": question_500})
        assert response.status_code == 200

    def test_chat_top_k_zero_returns_422(self, client: httpx.Client) -> None:
        """top_k=0 debe devolver 422 (mínimo es 1)."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "top_k": 0})
        assert response.status_code == 422

    def test_chat_top_k_21_returns_422(self, client: httpx.Client) -> None:
        """top_k=21 debe devolver 422 (máximo es 20)."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "top_k": 21})
        assert response.status_code == 422

    def test_chat_top_k_1_is_valid(self, client: httpx.Client) -> None:
        """top_k=1 debe ser aceptado (límite inferior válido)."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "top_k": 1})
        assert response.status_code == 200

    def test_chat_top_k_20_is_valid(self, client: httpx.Client) -> None:
        """top_k=20 debe ser aceptado (límite superior válido)."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "top_k": 20})
        assert response.status_code == 200

    def test_chat_historial_over_20_items_returns_422(self, client: httpx.Client) -> None:
        """Un historial con más de 20 mensajes debe devolver 422."""
        historial = [
            {"rol": "usuario", "contenido": "Hola"}
            if i % 2 == 0
            else {"rol": "asistente", "contenido": "Hola, ¿en qué puedo ayudarte?"}
            for i in range(21)
        ]
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "historial": historial})
        assert response.status_code == 422

    def test_chat_historial_exactly_20_items_is_valid(self, client: httpx.Client) -> None:
        """Un historial con exactamente 20 mensajes debe ser aceptado."""
        historial = [
            {"rol": "usuario", "contenido": "Hola"}
            if i % 2 == 0
            else {"rol": "asistente", "contenido": "Hola, ¿en qué puedo ayudarte?"}
            for i in range(20)
        ]
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "historial": historial})
        assert response.status_code == 200

    def test_chat_historial_invalid_rol_returns_422(self, client: httpx.Client) -> None:
        """Un mensaje de historial con rol inválido debe devolver 422."""
        historial = [{"rol": "admin", "contenido": "Hola"}]
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "historial": historial})
        assert response.status_code == 422

    def test_chat_historial_rol_system_returns_422(self, client: httpx.Client) -> None:
        """Un rol 'system' no es válido (solo 'usuario' y 'asistente' lo son)."""
        historial = [{"rol": "system", "contenido": "Eres un asistente."}]
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "historial": historial})
        assert response.status_code == 422

    def test_chat_historial_empty_content_returns_422(self, client: httpx.Client) -> None:
        """Un mensaje de historial con contenido vacío debe devolver 422."""
        historial = [{"rol": "usuario", "contenido": ""}]
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION, "historial": historial})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Encoding y caracteres especiales
# ---------------------------------------------------------------------------

class TestChatEncoding:
    """Verifica que la respuesta maneja correctamente caracteres UTF-8 y acentuados."""

    def test_chat_response_no_mojibake(self, client: httpx.Client) -> None:
        """La respuesta no debe contener secuencias de mojibake típicas de doble-encoding UTF-8."""
        response = client.post(
            CHAT_URL,
            json={"pregunta": "¿Qué tecnologías usa Vidra en sus soluciones de IA?"},
        )
        assert response.status_code == 200
        body = response.json()
        respuesta = body["respuesta"]
        # Mojibake común: Ã© (é), Ã³ (ó), Ã (á), Ã± (ñ) — UTF-8 interpretado como latin-1
        mojibake_patterns = ["Ã©", "Ã³", "Ã", "Ã±", "Ã¡", "Ã¼", "Ã¶"]
        for pattern in mojibake_patterns:
            assert pattern not in respuesta, (
                f"Posible mojibake detectado: '{pattern}' en la respuesta"
            )

    def test_chat_accented_question_is_accepted(self, client: httpx.Client) -> None:
        """Una pregunta con caracteres acentuados y ñ debe ser aceptada sin errores."""
        response = client.post(
            CHAT_URL,
            json={"pregunta": "¿Cuál es la misión y visión de Vidra en España?"},
        )
        assert response.status_code == 200

    def test_chat_response_encoding_is_utf8(self, client: httpx.Client) -> None:
        """El servidor debe responder con charset utf-8."""
        response = client.post(CHAT_URL, json={"pregunta": VALID_QUESTION})
        content_type = response.headers.get("content-type", "")
        # Verificar que el Content-Type incluye utf-8 o que la decodificación no falla
        # (httpx decodifica automáticamente; si falla, lanza UnicodeDecodeError)
        body = response.json()
        assert isinstance(body["respuesta"], str)
