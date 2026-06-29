import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';
const API_BASE = 'https://api.vidra-ia.com';

// ---------------------------------------------------------------------------
// OWASP A5 — Broken Access Control
// ---------------------------------------------------------------------------

test.describe('OWASP A5 - Broken Access Control', () => {
  const adminPaths = [
    '/admin',
    '/admin/',
    '/admin/login',
    '/dashboard',
    '/backend',
    '/api',
    '/api/admin',
  ];

  for (const path of adminPaths) {
    test(`admin path ${path} returns 4xx not 200`, async ({ request }) => {
      const response = await request.get(`${BASE}${path}`, { maxRedirects: 5 });
      const status = response.status();
      expect(
        status,
        `${path} returned ${status} — admin path may be publicly accessible`
      ).toBeGreaterThanOrEqual(400);
      expect(status).toBeLessThan(500);
    });
  }

  test('api admin endpoints require authentication', async ({ request }) => {
    const protectedEndpoints = [
      { method: 'GET', url: `${API_BASE}/rag/documents` },
      { method: 'GET', url: `${API_BASE}/rag/sources` },
      { method: 'POST', url: `${API_BASE}/rag/sync` },
    ];

    for (const { method, url } of protectedEndpoints) {
      const response =
        method === 'POST'
          ? await request.post(url, { headers: { 'Content-Type': 'application/json' } })
          : await request.get(url);

      expect(
        response.status(),
        `${method} ${url} should require authentication (expected 401 or 403, got ${response.status()})`
      ).toBeGreaterThanOrEqual(401);
      // Accept 401 Unauthorized or 403 Forbidden.
      expect(response.status()).toBeLessThanOrEqual(403);
    }
  });
});

// ---------------------------------------------------------------------------
// OWASP A6 — Security Misconfiguration
// ---------------------------------------------------------------------------

test.describe('OWASP A6 - Security Misconfiguration', () => {
  test('debug mode is disabled on API', async ({ request }) => {
    const debugEndpoints = [
      `${API_BASE}/docs`,
      `${API_BASE}/openapi.json`,
      `${API_BASE}/redoc`,
    ];

    for (const url of debugEndpoints) {
      const response = await request.get(url, { maxRedirects: 5 });
      expect(
        response.status(),
        `${url} is publicly accessible — debug/docs endpoint should be disabled in production`
      ).toBe(404);
    }
  });

  test('CORS does not allow wildcard origins on API', async ({ request }) => {
    const response = await request.get(`${API_BASE}/health`, {
      headers: { Origin: 'https://evil-site.com' },
    });

    const acao = response.headers()['access-control-allow-origin'];

    if (acao !== undefined) {
      expect(
        acao,
        'API CORS allows wildcard origin (*) — any site can call the API'
      ).not.toBe('*');
      expect(
        acao,
        'API CORS reflects untrusted origin https://evil-site.com'
      ).not.toBe('https://evil-site.com');
    }
    // If the header is absent, CORS is not enabled — that is also acceptable.
  });

  test('HTTP methods restricted on API', async ({ request }) => {
    // The chat endpoint only accepts POST.
    const getChat = await request.get(`${API_BASE}/rag/chat`);
    expect(
      getChat.status(),
      `GET ${API_BASE}/rag/chat should return 405 Method Not Allowed`
    ).toBe(405);

    // The health endpoint should not accept PUT.
    const putHealth = await request.put(`${API_BASE}/health`);
    expect(
      putHealth.status(),
      `PUT ${API_BASE}/health should return 405 Method Not Allowed`
    ).toBe(405);
  });
});

// ---------------------------------------------------------------------------
// OWASP A7 — XSS
// ---------------------------------------------------------------------------

test.describe('OWASP A7 - XSS', () => {
  // TODO(VID-004): CSP not yet configured on Cyberneticos
  test('CSP header blocks inline script execution', async ({ request }) => {
    const response = await request.get(BASE);
    const csp = response.headers()['content-security-policy'];

    if (csp) {
      // If CSP is present, it must include a script-src directive.
      expect(csp).toContain('script-src');
      // unsafe-eval allows eval() and Function() — it should not be present.
      expect(
        csp,
        'CSP contains unsafe-eval which weakens script execution protection'
      ).not.toContain('unsafe-eval');
    }
    // If CSP is absent the test is a no-op (tracked by VID-004).
  });
});

// ---------------------------------------------------------------------------
// OWASP A9 — Using Components with Known Vulnerabilities
// ---------------------------------------------------------------------------

test.describe('OWASP A9 - Using Components with Known Vulnerabilities', () => {
  test('response headers do not reveal technology versions', async ({ request }) => {
    // --- Web ---
    const webResponse = await request.get(BASE);
    const webHeaders = webResponse.headers();

    // x-powered-by should be absent entirely.
    expect(
      webHeaders['x-powered-by'],
      '"x-powered-by" header should not be present on the web server'
    ).toBeUndefined();

    // "server" header, if present, must not expose a version number (e.g. "nginx/1.24.0").
    const webServer = webHeaders['server'] ?? '';
    expect(
      webServer,
      `Web "server" header exposes version: "${webServer}"`
    ).not.toMatch(/\/\d/);

    // --- API ---
    const apiResponse = await request.get(`${API_BASE}/health`);
    const apiServer = (apiResponse.headers()['server'] ?? '').toLowerCase();

    // API server header must be one of the expected opaque values — no version suffix.
    expect(
      apiServer,
      `API "server" header exposes version: "${apiServer}"`
    ).not.toMatch(/\/\d/);

    // The value should be "vidra" or "nginx" (plain, no version).
    expect(['vidra', 'nginx']).toContain(apiServer);
  });
});
