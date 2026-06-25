"""Interfaz base de los publishers. Todos respetan dry_run."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.content.config import TenantConfig
from app.content.models import Article, PublishResult, SocialVariant


class BasePublisher(ABC):
    channel: str = "base"

    def __init__(self, tenant: TenantConfig, dry_run: bool = True) -> None:
        self.tenant = tenant
        self.dry_run = dry_run
        self.config = tenant.channels.get(self.channel, {})

    @abstractmethod
    def publish_article(self, article: Article) -> PublishResult:
        """Publica el artículo web. Solo lo implementan los canales web."""
        raise NotImplementedError

    @abstractmethod
    def publish_social(self, variant: SocialVariant) -> PublishResult:
        """Publica una variante social."""
        raise NotImplementedError

    # Helpers comunes -------------------------------------------------------
    def _dry(self, message: str, url: str | None = None) -> PublishResult:
        return PublishResult(channel=self.channel, success=True, dry_run=True,
                             url=url, message=f"[DRY-RUN] {message}")
