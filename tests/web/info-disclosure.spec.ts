import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';
const API_BASE = 'https://api.vidra-ia.com';

// ---------------------------------------------------------------------------
// Sensitive file access
// ---------------------------------------------------------------------------

test.describe('Sensitive file access', () => {
  const sensitivePaths = [
    '/.env',
    '/.env.local',
    '/.env.production',
    '/.git/config',
    '/.git/HEAD',
    '/.gitignore',
    '/config.php',
    '/wp-config.php',
    '/wp-login.php',
    '/admin/config',
    '/backend/app/settings.py',
    '/backup.sql',
    '/dump.sql',
    '/database.sql',
    '/config.json',
    '/secrets.json',
    '/.ssh/id_rsa',
    '/.ssh/authorized_keys',
    '/docker-compose.yml',
    '/docker-compose.prod.yml',
    '/Dockerfile',
    '/.DS_Store',
    '/package.json',
    '/composer.json',
    '/phpinfo.php',
    '/info.php',
    '/test.php',
  ];

  for (const path of sensitivePaths) {
    test(`sensitive file ${path} returns 403 or 404 not 200`, async ({ request }) => {
      const response = await request.get(`${BASE}${path}`, { maxRedirects: 5 });
      const status = response.status();
      expect(
        status,
        `${path} returned ${status} — sensitive file may be publicly accessible`
      ).not.toBe(200);
      expect([403, 404]).toContain(status);
    });
  }

  test('source map files are not publicly served', async ({ request }) => {
    const homeResponse = await request.get(BASE);
    const html = await homeResponse.text();

    // Extract all <script src="..."> values.
    const scriptSrcRegex = /<script[^>]+src=["']([^"']+\.js[^"']*)["']/gi;
    const scriptUrls: string[] = [];
    let match: RegExpExecArray | null;
    while ((match = scriptSrcRegex.exec(html)) !== null) {
      const src = match[1];
      // Resolve relative URLs against BASE.
      const url = src.startsWith('http') ? src : `${BASE}${src.startsWith('/') ? '' : '/'}${src}`;
      scriptUrls.push(url);
    }

    const exposedMaps: string[] = [];
    await Promise.all(
      scriptUrls.map(async (jsUrl) => {
        const mapUrl = `${jsUrl}.map`;
        const mapResponse = await request.get(mapUrl, { maxRedirects: 5 });
        if (mapResponse.status() === 200) {
          const body = await mapResponse.text();
          // A genuine source map is typically > 1 KB.
          if (body.length > 1024) {
            exposedMaps.push(mapUrl);
          }
        }
      })
    );

    expect(
      exposedMaps,
      `Source maps publicly accessible (exposes source code): ${exposedMaps.join(', ')}`
    ).toHaveLength(0);
  });
});

// ---------------------------------------------------------------------------
// Error page information disclosure
// ---------------------------------------------------------------------------

test.describe('Error page information disclosure', () => {
  const serverSignatures = ['nginx/', 'Apache/', 'Python/', 'uvicorn', 'node.js/'];

  test('404 page does not expose server version', async ({ request }) => {
    const response = await request.get(`${BASE}/this-page-does-not-exist-at-all`, {
      maxRedirects: 5,
    });
    const body = await response.text();

    for (const signature of serverSignatures) {
      expect(
        body,
        `404 response body exposes server signature: "${signature}"`
      ).not.toContain(signature);
    }
  });

  test('404 page is the custom Astro page not nginx default', async ({ request }) => {
    const response = await request.get(`${BASE}/non-existent-page-xyz`, {
      maxRedirects: 5,
    });

    expect(response.status()).toBe(404);

    const contentType = response.headers()['content-type'] ?? '';
    expect(contentType).toContain('text/html');

    const body = await response.text();
    expect(body.toLowerCase()).toContain('vidra');
  });

  test('directory listing is disabled', async ({ request }) => {
    const candidates = ['/assets/', '/images/'];

    for (const dir of candidates) {
      const response = await request.get(`${BASE}${dir}`, { maxRedirects: 5 });
      // Only check the body if the server actually responded with 200.
      if (response.status() === 200) {
        const body = await response.text();
        expect(
          body,
          `Directory listing may be enabled at ${dir} — "Index of " found in response`
        ).not.toContain('Index of ');
      }
      // 403/404 means listing is disabled — that is fine.
    }
  });
});

// ---------------------------------------------------------------------------
// API information disclosure
// ---------------------------------------------------------------------------

test.describe('API information disclosure', () => {
  test('api 404 returns JSON not HTML', async ({ request }) => {
    const response = await request.get(`${API_BASE}/non-existent-endpoint`, {
      maxRedirects: 5,
    });

    expect(response.status()).toBe(404);

    const contentType = response.headers()['content-type'] ?? '';
    expect(contentType).toContain('application/json');

    const text = await response.text();
    expect(() => JSON.parse(text)).not.toThrow();
  });

  test('api does not expose internal paths in error responses', async ({ request }) => {
    const response = await request.post(`${API_BASE}/rag/chat`, {
      data: { pregunta: null },
      headers: { 'Content-Type': 'application/json' },
    });

    expect(response.status()).toBe(422);

    const body = await response.text();
    const internalPathPatterns = ['/app/', 'app/main.py', 'site-packages', 'uvicorn'];
    for (const pattern of internalPathPatterns) {
      expect(
        body,
        `API error response leaks internal path: "${pattern}"`
      ).not.toContain(pattern);
    }
  });

  test('api server header hides implementation details', async ({ request }) => {
    const response = await request.get(`${API_BASE}/health`);

    const serverHeader = (response.headers()['server'] ?? '').toLowerCase();

    const implementationSignatures = ['uvicorn', 'python', 'fastapi'];
    for (const sig of implementationSignatures) {
      expect(
        serverHeader,
        `API "server" header reveals implementation detail: "${sig}"`
      ).not.toContain(sig);
    }

    // The server header should be "vidra" or plain "nginx" (without version).
    expect(['vidra', 'nginx']).toContain(serverHeader);
  });
});
