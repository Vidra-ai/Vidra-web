"""
Flujo OAuth 2.0 de LinkedIn — obtiene el access token y lo escribe en el .env del repo.

⚠️  ESTADO: PENDIENTE / NO OPERATIVO.
    La publicación en LinkedIn está bloqueada a la espera de la aprobación de la
    "Community Management API" (publicar como organización) y/o de un token válido.
    Este script queda preparado para cuando se desbloquee. Mientras tanto, el motor
    genera igualmente el texto del post (output en backend/content_output/<slug>.linkedin.txt)
    para publicarlo a mano.

Uso (cuando esté operativo, desde la carpeta backend/):
    python scripts/linkedin_auth.py

Qué hace:
  1. Abre el navegador en la URL de autorización de LinkedIn.
  2. Levanta un servidor local en http://localhost:8080 para capturar el callback.
  3. Intercambia el código por un access token.
  4. Obtiene el URN del perfil o la organización.
  5. Escribe LINKEDIN_ACCESS_TOKEN y LINKEDIN_AUTHOR_URN en el .env del repo.

Requisito previo:
  En LinkedIn Developer Portal → tu app → Auth → Authorized redirect URLs,
  añade exactamente: http://localhost:8080/callback
"""

from __future__ import annotations

import os
import re
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# ── Scopes necesarios ────────────────────────────────────────────────────────
# w_member_social        → publicar como persona (Share on LinkedIn)
# w_organization_social  → publicar como organización (Community Management API — solicitar si falta)
# openid + offline_access → identificación + refresh token automático
SCOPES = "openid offline_access w_member_social"

REDIRECT_URI = "http://localhost:8080/callback"
AUTH_URL     = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL    = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL  = "https://api.linkedin.com/v2/userinfo"

# scripts/linkedin_auth.py -> parents[0]=scripts, [1]=backend, [2]=raíz del repo
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

# ── Estado compartido entre el servidor y el hilo principal ─────────────────
_result: dict = {}


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            _result["code"] = params["code"][0]
            _result["state"] = params.get("state", [""])[0]
            body = b"<h2>Autorizacion completada. Puedes cerrar esta pestana.</h2>"
            status = 200
        else:
            _result["error"] = params.get("error", ["desconocido"])[0]
            body = b"<h2>Error en la autorizacion. Revisa la terminal.</h2>"
            status = 400

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # silenciar logs del servidor


def _exchange_code(code: str, client_id: str, client_secret: str) -> dict:
    """Intercambia el código de autorización por un access token."""
    import json

    data = urllib.parse.urlencode({
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  REDIRECT_URI,
        "client_id":     client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def _get_profile_urn(access_token: str) -> str:
    """Obtiene el URN del miembro (urn:li:person:XXXXX)."""
    import json

    req = urllib.request.Request(
        PROFILE_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    # openid devuelve `sub` = ID numérico del miembro
    sub = data.get("sub", "")
    return f"urn:li:person:{sub}" if sub else ""


def _update_env(key: str, value: str) -> None:
    """Actualiza o añade una clave en el .env sin tocar el resto."""
    text = ENV_FILE.read_text(encoding="utf-8") if ENV_FILE.exists() else ""
    pattern = rf"^{re.escape(key)}=.*$"
    replacement = f"{key}={value}"
    if re.search(pattern, text, flags=re.MULTILINE):
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    else:
        text = text.rstrip("\n") + f"\n{replacement}\n"
    ENV_FILE.write_text(text, encoding="utf-8")
    print(f"  OK {key} actualizado en {ENV_FILE}")


def main() -> None:
    # Carga CLIENT_ID y CLIENT_SECRET del .env
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)

    client_id     = os.environ.get("CLIENT_ID", "")
    client_secret = os.environ.get("CLIENT_SECRET", "")

    if not client_id or not client_secret:
        sys.exit("Error: CLIENT_ID y CLIENT_SECRET deben estar en el .env")

    state = secrets.token_urlsafe(16)

    auth_params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id":     client_id,
        "redirect_uri":  REDIRECT_URI,
        "scope":         SCOPES,
        "state":         state,
    })
    url = f"{AUTH_URL}?{auth_params}"

    print("\n-- LinkedIn OAuth 2.0 --------------------------------")
    print("Abriendo el navegador para autorizar la aplicacion...")
    print(f"Si no se abre automaticamente, copia esta URL:\n  {url}\n")
    webbrowser.open(url)

    # Levanta el servidor local y espera el callback
    server = HTTPServer(("localhost", 8080), _CallbackHandler)
    print("Esperando callback en http://localhost:8080/callback ...")
    server.handle_request()  # una sola petición
    server.server_close()

    if "error" in _result:
        sys.exit(f"Error de autorizacion: {_result['error']}")

    if _result.get("state") != state:
        sys.exit("Error: state no coincide (posible CSRF). Vuelve a intentarlo.")

    code = _result["code"]
    print("\nCodigo recibido. Obteniendo access token...")

    token_data = _exchange_code(code, client_id, client_secret)
    access_token = token_data.get("access_token", "")
    expires_in   = token_data.get("expires_in", "desconocido")

    if not access_token:
        sys.exit(f"No se obtuvo access_token. Respuesta: {token_data}")

    print(f"Token obtenido (expira en {expires_in} segundos ~ {int(expires_in)//86400} dias)")

    print("Obteniendo URN del perfil...")
    urn = _get_profile_urn(access_token)
    if urn:
        print(f"URN: {urn}")
    else:
        print("No se pudo obtener el URN — escribe manualmente LINKEDIN_AUTHOR_URN en .env")

    refresh_token         = token_data.get("refresh_token", "")
    refresh_expires_in    = token_data.get("refresh_token_expires_in", "")

    print("\nGuardando en .env...")
    _update_env("LINKEDIN_ACCESS_TOKEN", access_token)
    if refresh_token:
        _update_env("LINKEDIN_REFRESH_TOKEN", refresh_token)
        days = int(refresh_expires_in) // 86400 if refresh_expires_in else "?"
        print(f"  OK Refresh token guardado (expira en ~{days} dias)")
    else:
        print("  AVISO: no se recibio refresh token. El access token debera renovarse manualmente.")
    if urn:
        _update_env("LINKEDIN_AUTHOR_URN", urn)

    print("\nListo. Ya puedes publicar en LinkedIn con el motor de contenido.")


if __name__ == "__main__":
    main()
