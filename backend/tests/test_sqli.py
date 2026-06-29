"""Tests de integración para inyección SQL contra POST /rag/chat.

La API usa SQLAlchemy ORM con pgvector, por lo que todas las queries son
parametrizadas. El objetivo de estos tests es verificar que ningún payload
SQLi provoca un 500 ni filtra mensajes de error de base de datos, y que los
payloads basados en tiempo (SLEEP / pg_sleep) no retrasan la respuesta más
de 30 segundos.
"""

import time

import httpx
import pytest

CHAT_URL = "/rag/chat"

# Payloads SQLi con nombre descriptivo para identificar fallos en el report
SQLI_PAYLOADS = [
    ("basic_single_quote", "'"),
    ("or_true_string", "' OR '1'='1"),
    ("or_true_comment", "' OR 1=1--"),
    ("drop_table", "'; DROP TABLE rag_documents;--"),
    ("union_null", "' UNION SELECT NULL,NULL,NULL--"),
    ("double_quote", '" OR "1"="1'),
    ("mysql_sleep", "1' AND SLEEP(5)--"),
    ("pg_sleep", "1' AND pg_sleep(5)--"),
    ("cast_version", "' AND 1=CAST((SELECT version()) AS int)--"),
    ("pg_sleep_stack", "'; SELECT pg_sleep(5);--"),
    ("admin_comment", "admin'--"),
    ("or_empty", "' OR ''='"),
]

# Solo los payloads que intentan provocar un retardo en la base de datos
SLEEP_PAYLOAD_NAMES = {"mysql_sleep", "pg_sleep", "pg_sleep_stack"}

# Subcadenas que indican que el error de BD llegó hasta el cliente
SQL_ERROR_STRINGS = [
    "ERROR:",
    "syntax error",
    "pg_",
    "ORA-",
    "MySQL",
    "MSSQL",
    "sqlite",
]


class TestSQLiNoCrash:
    """Verifica que ningún payload SQLi provoca 500 ni expone mensajes de error de BD."""

    @pytest.mark.parametrize("name,payload", SQLI_PAYLOADS, ids=[p[0] for p in SQLI_PAYLOADS])
    def test_sqli_does_not_return_500(self, client: httpx.Client, name: str, payload: str) -> None:
        """El endpoint no debe devolver 500 ante payloads SQLi; el ORM los parametriza."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        assert response.status_code != 500, (
            f"Payload '{name}' causó HTTP 500. Posible fuga de excepción de BD.\n"
            f"Body: {response.text[:500]}"
        )

    @pytest.mark.parametrize("name,payload", SQLI_PAYLOADS, ids=[p[0] for p in SQLI_PAYLOADS])
    def test_sqli_response_does_not_contain_sql_error_strings(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """El cuerpo de la respuesta no debe contener cadenas de error propias de motores SQL."""
        response = client.post(CHAT_URL, json={"pregunta": payload})
        body_text = response.text
        for error_string in SQL_ERROR_STRINGS:
            assert error_string not in body_text, (
                f"Payload '{name}': la respuesta contiene '{error_string}', "
                f"lo que indica una fuga de error de base de datos.\n"
                f"Body (primeros 500 chars): {body_text[:500]}"
            )


class TestSQLiTimeBased:
    """Verifica que los payloads con SLEEP / pg_sleep no retrasan la respuesta.

    Si el ORM parametriza correctamente las queries, los sleeps no se ejecutan
    en la BD y la respuesta debe llegar en menos de 30 segundos (umbral generoso
    para incluir latencia de red y tiempo del LLM).
    """

    SLEEP_PAYLOADS = [
        (name, payload)
        for name, payload in SQLI_PAYLOADS
        if name in SLEEP_PAYLOAD_NAMES
    ]

    @pytest.mark.parametrize(
        "name,payload",
        SLEEP_PAYLOADS,
        ids=[p[0] for p in SLEEP_PAYLOADS],
    )
    def test_sleep_payload_response_time_under_30s(
        self, client: httpx.Client, name: str, payload: str
    ) -> None:
        """Los payloads con SLEEP/pg_sleep no deben retrasar la respuesta más de 30 segundos."""
        start = time.time()
        response = client.post(CHAT_URL, json={"pregunta": payload}, timeout=60.0)
        elapsed = time.time() - start

        assert elapsed < 30.0, (
            f"Payload '{name}' tardó {elapsed:.1f}s (> 30s). "
            f"Es posible que pg_sleep se esté ejecutando en la base de datos."
        )
        assert response.status_code != 500, (
            f"Payload '{name}' causó HTTP 500 tras {elapsed:.1f}s."
        )
