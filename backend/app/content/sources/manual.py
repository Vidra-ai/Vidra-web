"""Entradas manuales: "lo que hemos hecho" (proyectos, casos, notas)."""

from __future__ import annotations

from app.content.models import Topic, TopicOrigin
from app.content.sources.base import BaseSource


class ManualSource(BaseSource):
    """Convierte texto aportado por la empresa en un tema.

    No descubre nada por su cuenta: recibe el texto y lo envuelve como `Topic`.
    Útil para "hemos implantado X", "caso de éxito con cliente Y", etc.
    """

    name = "manual"

    def __init__(self, tenant, text: str = "", title: str = "") -> None:
        super().__init__(tenant)
        self.text = text
        self.title = title

    def discover(self, limit: int = 5) -> list[Topic]:
        if not self.text:
            return []
        return [
            Topic(
                title=self.title or self.text[:80],
                summary=self.text,
                origin=TopicOrigin.MANUAL,
                raw=self.text,
            )
        ]
