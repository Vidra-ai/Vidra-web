"""Publicación en LinkedIn vía UGC Posts API con refresco automático de token."""

from __future__ import annotations

import re
import time

from app.content import paths
from app.content.config import env
from app.content.models import Article, PublishResult, SocialVariant
from app.content.publishers.base import BasePublisher
from app.content.utils.logging import get_logger

log = get_logger()

POSTS_URL   = "https://api.linkedin.com/v2/ugcPosts"
TOKEN_URL   = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL = "https://api.linkedin.com/v2/userinfo"

# Renueva el token si le quedan menos de 7 días
_RENEW_BEFORE_EXPIRY_SEC = 7 * 24 * 3600


class LinkedInPublisher(BasePublisher):
    channel = "linkedin"

    def publish_article(self, article: Article) -> PublishResult:
        raise NotImplementedError("LinkedIn es canal social; usa publish_social().")

    def publish_social(self, variant: SocialVariant) -> PublishResult:
        text = _with_hashtags(variant.text, variant.hashtags)

        if self.dry_run:
            return self._dry(f"Publicaría en LinkedIn:\n{text}")

        token = _ensure_fresh_token()
        if not token:
            return PublishResult(
                channel=self.channel, success=False,
                message="Falta LINKEDIN_ACCESS_TOKEN en .env. "
                        "Ejecuta: python backend/scripts/linkedin_auth.py",
            )

        author = env("LINKEDIN_AUTHOR_URN")
        if not author:
            return PublishResult(
                channel=self.channel, success=False,
                message="Falta LINKEDIN_AUTHOR_URN en .env.",
            )

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        if variant.link:
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "ARTICLE"
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {"status": "READY", "originalUrl": variant.link}
            ]

        try:
            import httpx
            resp = httpx.post(
                POSTS_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0",
                },
                timeout=15,
            )
            resp.raise_for_status()
            post_id  = resp.headers.get("x-restli-id", "")
            post_url = f"https://www.linkedin.com/feed/update/{post_id}" if post_id else None
            log.info("[linkedin] Publicado. ID: %s", post_id)
            return PublishResult(
                channel=self.channel, success=True,
                url=post_url, external_id=post_id,
                message=f"Publicado en LinkedIn. ID: {post_id}",
            )
        except Exception as exc:
            log.error("[linkedin] Error al publicar: %s", exc)
            return PublishResult(channel=self.channel, success=False,
                                 message=f"Error al publicar en LinkedIn: {exc}")


# ── Refresco automático ───────────────────────────────────────────────────────

def _ensure_fresh_token() -> str | None:
    """Devuelve un access token válido, renovándolo si está próximo a caducar."""
    token         = env("LINKEDIN_ACCESS_TOKEN")
    refresh_token = env("LINKEDIN_REFRESH_TOKEN")
    expires_at    = env("LINKEDIN_TOKEN_EXPIRES_AT")  # epoch int guardado al obtener/renovar

    if not token:
        return None

    # Si no sabemos cuándo expira o le quedan menos de 7 días → intentar renovar
    needs_refresh = False
    if expires_at:
        try:
            needs_refresh = (int(expires_at) - time.time()) < _RENEW_BEFORE_EXPIRY_SEC
        except ValueError:
            needs_refresh = False
    # Si no hay expires_at guardado, confiamos en el token actual (primera vez)

    if needs_refresh and refresh_token:
        log.info("[linkedin] Access token próximo a caducar — renovando automáticamente...")
        new_token = _refresh_access_token(refresh_token)
        if new_token:
            return new_token

    return token


def _refresh_access_token(refresh_token: str) -> str | None:
    """Usa el refresh token para obtener un nuevo access token y lo guarda en .env."""
    import json
    import urllib.parse
    import urllib.request

    client_id     = env("CLIENT_ID", "")
    client_secret = env("CLIENT_SECRET", "")

    if not client_id or not client_secret:
        log.warning("[linkedin] CLIENT_ID / CLIENT_SECRET no configurados; no se puede renovar.")
        return None

    data = urllib.parse.urlencode({
        "grant_type":    "refresh_token",
        "refresh_token": refresh_token,
        "client_id":     client_id,
        "client_secret": client_secret,
    }).encode()

    try:
        req = urllib.request.Request(
            TOKEN_URL, data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_data = json.loads(resp.read())
    except Exception as exc:
        log.error("[linkedin] Error al renovar token: %s", exc)
        return None

    new_access  = token_data.get("access_token", "")
    new_refresh = token_data.get("refresh_token", "")
    expires_in  = token_data.get("expires_in", 0)

    if not new_access:
        log.error("[linkedin] Respuesta de renovación sin access_token: %s", token_data)
        return None

    expires_at = int(time.time()) + int(expires_in)
    _update_env("LINKEDIN_ACCESS_TOKEN",    new_access)
    _update_env("LINKEDIN_TOKEN_EXPIRES_AT", str(expires_at))
    if new_refresh:
        _update_env("LINKEDIN_REFRESH_TOKEN", new_refresh)

    log.info("[linkedin] Token renovado correctamente (expira en %d días).",
             int(expires_in) // 86400)
    return new_access


def _update_env(key: str, value: str) -> None:
    """Actualiza o añade una clave en el .env del repo."""
    env_path = paths.env_file()
    text = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
    pattern = rf"^{re.escape(key)}=.*$"
    replacement = f"{key}={value}"
    if re.search(pattern, text, flags=re.MULTILINE):
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    else:
        text = text.rstrip("\n") + f"\n{replacement}\n"
    env_path.write_text(text, encoding="utf-8")


def _with_hashtags(text: str, hashtags: list[str]) -> str:
    tags = " ".join(h if h.startswith("#") else f"#{h}" for h in hashtags)
    return f"{text}\n\n{tags}".strip()
