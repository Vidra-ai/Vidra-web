"""Tests de integración para el endpoint GET /health."""

import time

import httpx
import pytest


def test_health_returns_200(client: httpx.Client) -> None:
    """GET /health debe devolver HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status(client: httpx.Client) -> None:
    """El cuerpo de /health debe ser exactamente {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type_is_json(client: httpx.Client) -> None:
    """GET /health debe responder con Content-Type application/json."""
    response = client.get("/health")
    assert "application/json" in response.headers.get("content-type", "")


def test_health_response_time_under_3s(client: httpx.Client) -> None:
    """GET /health debe responder en menos de 3 segundos."""
    start = time.monotonic()
    client.get("/health")
    elapsed = time.monotonic() - start
    assert elapsed < 3.0, f"El endpoint /health tardó {elapsed:.2f}s (límite: 3s)"


def test_health_schema_has_only_status_key(client: httpx.Client) -> None:
    """La respuesta de /health no debe contener claves extras."""
    body = client.get("/health").json()
    assert set(body.keys()) == {"status"}


def test_health_status_value_is_string(client: httpx.Client) -> None:
    """El valor del campo 'status' en /health debe ser un string."""
    body = client.get("/health").json()
    assert isinstance(body["status"], str)
