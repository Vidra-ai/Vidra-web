"""Descubrimiento de temas a partir de feeds RSS con estrategia por niveles.

Nivel 1 — priority_feeds: revistas/medios prioritarios del sector, mayor autoridad.
Nivel 2 — google_news_feeds: medios generalistas y Google News como fallback.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.content.models import Topic, TopicOrigin
from app.content.sources.base import BaseSource
from app.content.utils.logging import get_logger

log = get_logger()

DAYS_WINDOW = 3  # solo artículos publicados en los últimos N días


class RssSource(BaseSource):
    name = "rss"

    def discover(self, limit: int = 10) -> list[Topic]:
        try:
            import feedparser
        except ImportError:
            log.warning("feedparser no instalado; instala dependencias para usar RSS.")
            return []

        keywords = [k.lower() for k in self.tenant.sources.keywords_filter]
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=DAYS_WINDOW)

        # Nivel 1: feeds prioritarios del sector
        priority = self.tenant.sources.priority_feeds or self.tenant.sources.rss
        topics = self._read_feeds(feedparser, priority, keywords, limit, cutoff)
        log.info("Feeds prioritarios → %d temas (últimos %d días)", len(topics), DAYS_WINDOW)

        # Nivel 2: medios generalistas y Google News si no hay suficiente
        if len(topics) < limit:
            needed = limit - len(topics)
            fallback_topics = self._read_feeds(
                feedparser, self.tenant.sources.google_news_feeds, keywords, needed, cutoff,
            )
            log.info("Medios/Google News → %d temas adicionales", len(fallback_topics))
            seen = {t.title.lower() for t in topics}
            for t in fallback_topics:
                if t.title.lower() not in seen:
                    topics.append(t)
                    seen.add(t.title.lower())

        topics.sort(key=lambda t: t.published_at or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        return topics[:limit]

    def _read_feeds(
        self,
        feedparser,
        feeds: list[str],
        keywords: list[str],
        limit: int,
        cutoff: datetime,
    ) -> list[Topic]:
        topics: list[Topic] = []
        for url in feeds:
            if len(topics) >= limit * 2:
                break
            log.info("Leyendo feed: %s", url)
            try:
                parsed = feedparser.parse(url)
            except Exception as exc:
                log.warning("Error leyendo feed %s: %s", url, exc)
                continue

            for entry in parsed.entries:
                title = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")

                pub_date = _parse_date(entry)
                if pub_date and pub_date < cutoff:
                    continue  # artículo demasiado antiguo

                blob = f"{title} {summary}".lower()
                if keywords and not any(k in blob for k in keywords):
                    continue

                topics.append(Topic(
                    title=title,
                    summary=summary,
                    origin=TopicOrigin.NEWS,
                    source_url=getattr(entry, "link", None),
                    source_name=parsed.feed.get("title") if parsed.feed else url,
                    published_at=pub_date,
                    raw=summary,
                ))
        return topics


def _parse_date(entry) -> datetime | None:
    import time
    parsed = getattr(entry, "published_parsed", None)
    if parsed:
        try:
            return datetime.fromtimestamp(time.mktime(parsed), tz=timezone.utc)
        except (OverflowError, OSError):
            return None
    return None
