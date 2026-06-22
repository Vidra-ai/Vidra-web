# Despliegue del chatbot web

Stack del **chatbot público** de `vidra-ia.com`: API RAG (FastAPI) + PostgreSQL/pgvector.
La web Astro se sirve aparte (estática, vía Nginx). Aquí solo se despliega la API + su DB.

> Convenciones de infraestructura: ver Obsidian → *Arquitectura del servidor*,
> *Despliegues*, *Gestión de secretos*, *Red*. Servidor: `vidra-central`
> (Hetzner CCX23, 4 vCPU / 16 GB, `178.104.197.240`, SSH `55022`).

---

## 1. Validación local (hacer SIEMPRE antes de desplegar)

```bash
cp .env.example .env          # rellena OPENAI_API_KEY y ADMIN_API_KEY
docker compose up -d --build  # db + api + web dev server
```

- Web: http://localhost:4322/chat
- API: http://localhost:8001/health → `{"status":"ok"}`
- Indexar documentos locales (carpeta `backend/RAG/`):
  `docker compose exec api python -m app.rag.seed`

Comprobaciones:
- [ ] `/health` responde.
- [ ] El chat responde con documentos indexados.
- [ ] Sin docs, responde "No tengo información suficiente…".
- [ ] El panel `/admin/rag` carga con la `ADMIN_API_KEY`.
- [ ] Tras ~20 mensajes seguidos, la API devuelve 429 (rate limit).

---

## 2. Despliegue en vidra-central

Patrón ADR-006/ADR-007: imágenes desde **GHCR**, **no se construyen en el servidor**;
Nginx hace de proxy inverso + SSL; secretos en **Vaultwarden**; DB **no expuesta**.

### 2.1 Subdominio y DNS
Crear `chat-api.vidra-ia.com` (o el que se decida) → `178.104.197.240`.
La web (`vidra-ia.com`) se compila con `PUBLIC_API_URL=https://chat-api.vidra-ia.com`.

### 2.2 Imagen en GHCR
Construir y publicar `ghcr.io/vidra-ai/vidra-web-chatbot:<tag>` (idealmente vía GitHub
Actions con tag `v*`, igual que area-hub). Como puente manual:

```bash
docker build -t ghcr.io/vidra-ai/vidra-web-chatbot:latest ./backend
docker push ghcr.io/vidra-ai/vidra-web-chatbot:latest
```

### 2.3 En el servidor

```bash
ssh -p 55022 cdiaz@178.104.197.240
mkdir -p ~/vidra-chatbot && cd ~/vidra-chatbot
# copiar docker-compose.prod.yml y crear .env (valores desde Vaultwarden)
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec api python -m app.rag.seed
```

### 2.4 Nginx (vhost del subdominio API)
Bloque `server` para `chat-api.vidra-ia.com` → `proxy_pass http://127.0.0.1:8001;`
con cabeceras `X-Forwarded-For`/`X-Forwarded-Proto`. SSL con Certbot
(`certbot --nginx -d chat-api.vidra-ia.com`). Registrar en Obsidian → *Red* y *Despliegues*.

### 2.5 Secretos (Vaultwarden — nunca en git)
| Variable | Colección |
|---|---|
| `OPENAI_API_KEY` | 03 - Proveedores IA |
| `ADMIN_API_KEY`, `POSTGRES_PASSWORD` | 01 - Servidor Vidra |

---

## 3. Notas de escalabilidad / operación

- **Rate limit** (`/rag/chat`) es en memoria y por worker. Con `UVICORN_WORKERS=1`
  (default) el límite es exacto. Para >1 worker o varias réplicas, mover el contador
  a `vidra_redis` (ya existe en el servidor).
- **Índices pgvector**: `init_db()` crea índice HNSW (vectorial) + GIN trigram (léxico).
  Soportan crecimiento del corpus sin escaneo secuencial.
- **Coste OpenAI**: cada chat hace 1 embedding + 1 completion. El rate limit y el cap de
  longitud de entrada (pregunta ≤ 500, historial ≤ 20) acotan el gasto.
- **Backups**: el volumen `vidra_chatbot_pgdata` debe entrar en la estrategia de
  *Backups* (Obsidian). El corpus es reindexable, pero conviene respaldarlo igualmente.
- **Rollback**: `docker compose -f docker-compose.prod.yml up -d` con el tag anterior.
