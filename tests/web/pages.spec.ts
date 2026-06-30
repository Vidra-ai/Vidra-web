import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';

const PAGES = [
  '/',
  '/who-we-are',
  '/services',
  '/services/analysis',
  '/services/deep-learning',
  '/services/machine-learning',
  '/proyectos',
  '/blog',
  '/blog/ia-explicable-construccion-xai-metodos-aplicaciones-limites',
  '/blog/inteligencia-artificial-para-empresas-peru-adopcion-ejecutivos',
  '/blog/primer-post',
  '/faq',
  '/legal',
  '/contact',
  '/en/',
  '/en/who-we-are',
  '/en/services',
  '/en/services/analysis',
  '/en/services/deep-learning',
  '/en/services/machine-learning',
  '/en/projects',
  '/en/blog',
  '/en/faq',
  '/en/legal',
  '/en/contact',
];

test.describe('All sitemap pages return 200 with a title', () => {
  for (const path of PAGES) {
    test(`GET ${path}`, async ({ request, page }) => {
      const response = await request.get(`${BASE}${path}`);
      expect(response.status(), `Status for ${path}`).toBe(200);

      // Verify the page has a non-empty <title>
      await page.goto(`${BASE}${path}`);
      const title = await page.title();
      expect(title, `Title for ${path}`).toBeTruthy();
      expect(title.trim().length, `Title length for ${path}`).toBeGreaterThan(0);
    });
  }
});

test.describe('No 5xx errors on any page', () => {
  test('batch HEAD check — no server errors', async ({ request }) => {
    const results = await Promise.all(
      PAGES.map(async (path) => {
        const res = await request.head(`${BASE}${path}`);
        return { path, status: res.status() };
      })
    );

    const serverErrors = results.filter((r) => r.status >= 500);
    expect(
      serverErrors,
      `Pages with 5xx: ${serverErrors.map((r) => r.path).join(', ')}`
    ).toHaveLength(0);
  });
});
