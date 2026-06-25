"""Adaptadores de publicación por canal.

Solo se incluyen los canales necesarios para esta funcionalidad: el blog Astro
de Vidra (`vidra_md`) y LinkedIn. WordPress, X e Instagram se han dejado fuera a
propósito (ver el proyecto ContentPilot original si se quieren reincorporar).
"""

from app.content.publishers.base import BasePublisher
from app.content.publishers.linkedin import LinkedInPublisher
from app.content.publishers.vidra_md import VidraMdPublisher

REGISTRY: dict[str, type[BasePublisher]] = {
    "linkedin": LinkedInPublisher,
    "vidra_md": VidraMdPublisher,
}

__all__ = ["BasePublisher", "REGISTRY"]
