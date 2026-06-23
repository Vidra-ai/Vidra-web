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

### 2.1 Ruta en el dominio principal
La API se sirve bajo `https://vidra-ia.com/api/` — sin subdominio separado, mismo origen
que la web. No requiere registro DNS extra ni certificado SSL adicional.
La web se compila con `PUBLIC_API_URL=https://vidra-ia.com/api`.

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

### 2.4 Nginx (bloque /api/ en el vhost de vidra-ia.com)
Dentro del `server` existente de `vidra-ia.com`, añadir antes del bloque de archivos
estáticos:

```nginx
location /api/ {
    proxy_pass         http://127.0.0.1:8001/;
    proxy_set_header   Host              $host;
    proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_read_timeout 120s;
}
```

El trailing slash en `proxy_pass` hace que Nginx elimine el prefijo `/api` antes de
reenviar a FastAPI, que sigue viendo sus rutas normales (`/health`, `/rag/chat`, etc.).
No se necesita certificado ni vhost adicional. Registrar en Obsidian → *Despliegues*.

### 2.5 Secretos (Vaultwarden — nunca en git)
| Variable | Colección |
|---|---|
| `OPENAI_API_KEY` | 03 - Proveedores IA |
| `ADMIN_API_KEY`, `POSTGRES_PASSWORD` | 01 - Servidor Vidra |

---

## 3. Fuente de contenido: carpeta pública de Obsidian

El chatbot se nutre de la carpeta **"01 - Información pública (web - chatbot)"** del vault
(única fuente de verdad, ADR-005). El backend la lee montada en `/vault-publico` (solo
lectura) y la **sincroniza de forma incremental**: en cada ciclo (`PUBLIC_DOCS_SYNC_INTERVAL`
seg) calcula el hash de cada `.md` y **re-embebe solo los que cambian**; indexa los nuevos
y elimina del índice los borrados o los que dejan de ser públicos.

- Solo se indexan notas con frontmatter `visibilidad: publico` (`PUBLIC_DOCS_REQUIRE_PUBLIC_FLAG`).
- Se limpia el markdown antes de embeber: frontmatter, `#etiquetas`, callouts de aviso,
  `[[enlaces]]` y la sección "Notas relacionadas".
- Forzar una sincronización: `POST /rag/sync-public` con `X-Admin-Key`.

**Local:** se monta automáticamente desde `PUBLIC_DOCS_HOST_DIR` (MEGA) en compose.
**Servidor:** el vault aún no está en vidra-central (tarea pendiente "Obsidian bare repo").
Hasta entonces, `PUBLIC_DOCS_DIR` vacío deja la sincronización desactivada. Cuando el vault
esté disponible, descomenta el volumen en `docker-compose.prod.yml` y define
`PUBLIC_DOCS_DIR=/vault-publico` + `PUBLIC_DOCS_HOST_DIR=<ruta en el servidor>`.

## 4. Notas de escalabilidad / operación

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
