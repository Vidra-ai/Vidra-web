"""Interfaz base de las fuentes de temas."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.content.config import TenantConfig
from app.content.models import Topic


class BaseSource(ABC):
    """Toda fuente de temas implementa esta interfaz."""

    name: str = "base"

    def __init__(self, tenant: TenantConfig) -> None:
        self.tenant = tenant

    @abstractmethod
    def discover(self, limit: int = 5) -> list[Topic]:
        """Devuelve hasta `limit` temas candidatos."""
        raise NotImplementedError
