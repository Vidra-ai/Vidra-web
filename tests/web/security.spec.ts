import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';
const API_BASE = 'https://api.vidra-ia.com';

test.describe('HTTP → HTTPS redirect', () => {
  test('http://vidra-ia.com redirects to https with 301', async ({ request }) => {
    const response = await request.get('http://vidra-ia.com', {
      maxRedirects: 0,
    });
    expect(response.status()).toBe(301);
    const location = response.headers()['location'];
    expect(location).toMatch(/^https:\/\//);
  });
});

test.describe('Security headers — web', () => {
  let headers: Record<string, string>;

  test.beforeAll(async ({ request }) => {
    const response = await request.get(BASE);
    headers = response.headers();
  });

  // TODO(VID-004): pending Cyberneticos — HSTS not yet configured on the web server
  test('Strict-Transport-Security header present', async ({ request }) => {
    const response = await request.get(BASE);
    expect(response.headers()['strict-transport-security']).toBeTruthy();
  });

  // TODO(VID-004): pending Cyberneticos — X-Frame-Options not yet configured on the web server
  test('X-Frame-Options header present', async ({ request }) => {
    const response = await request.get(BASE);
    const value = response.headers()['x-frame-options'];
    expect(value).toBeTruthy();
    expect(value.toUpperCase()).toMatch(/^(DENY|SAMEORIGIN)$/);
  });

  // TODO(VID-004): pending Cyberneticos — X-Content-Type-Options not yet configured on the web server
  test('X-Content-Type-Options: nosniff present', async ({ request }) => {
    const response = await request.get(BASE);
    expect(response.headers()['x-content-type-options']).toBe('nosniff');
  });

  // TODO(VID-004): pending Cyberneticos — Content-Security-Policy not yet configured on the web server
  test('Content-Security-Policy header present', async ({ request }) => {
    const response = await request.get(BASE);
    expect(response.headers()['content-security-policy']).toBeTruthy();
  });
});

test.describe('Security headers — API', () => {
  test('API has Strict-Transport-Security', async ({ request }) => {
    const response = await request.get(API_BASE);
    expect(response.headers()['strict-transport-security']).toBeTruthy();
  });
});

test.describe('Sensitive paths blocked', () => {
  const blockedPaths = ['/admin', '/.env', '/.git', '/backup.sql'];

  for (const path of blockedPaths) {
    test(`${path} returns 403`, async ({ request }) => {
      const response = await request.get(`${BASE}${path}`, { maxRedirects: 5 });
      expect(response.status()).toBe(403);
    });
  }
});

test.describe('Well-known files', () => {
  test('security.txt exists and is accessible', async ({ request }) => {
    const response = await request.get(`${BASE}/.well-known/security.txt`);
    expect(response.status()).toBe(200);
    const text = await response.text();
    expect(text.length).toBeGreaterThan(0);
  });

  test('robots.txt exists, allows crawling, and references Sitemap', async ({ request }) => {
    const response = await request.get(`${BASE}/robots.txt`);
    expect(response.status()).toBe(200);
    const text = await response.text();
    expect(text).toContain('Sitemap:');
    expect(text).not.toContain('Disallow: /\n');
  });
});
