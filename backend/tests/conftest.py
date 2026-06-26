"""Configuración compartida para los tests de integración contra producción."""

import pytest
import httpx

BASE_URL = "https://api.vidra-ia.com"


@pytest.fixture(scope="session")
def client() -> httpx.Client:
    """Cliente HTTP síncrono con timeout generoso para llamadas a producción."""
    with httpx.Client(base_url=BASE_URL, timeout=15.0) as c:
        yield c
