import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';

/** Pages to check for basic SEO meta tags [path, expectedLang] */
const SEO_PAGES: [string, 'es' | 'en'][] = [
  ['/', 'es'],
  ['/who-we-are', 'es'],
  ['/services', 'es'],
  ['/proyectos', 'es'],
  ['/blog', 'es'],
  ['/faq', 'es'],
  ['/contact', 'es'],
  ['/en/', 'en'],
  ['/en/who-we-are', 'en'],
  ['/en/services', 'en'],
  ['/en/projects', 'en'],
  ['/en/blog', 'en'],
  ['/en/faq', 'en'],
  ['/en/contact', 'en'],
];

test.describe('Meta description present', () => {
  for (const [path] of SEO_PAGES) {
    test(path, async ({ page }) => {
      await page.goto(`${BASE}${path}`);
      const content = await page
        .locator('meta[name="description"]')
        .getAttribute('content');
      expect(content, `meta description on ${path}`).toBeTruthy();
      expect(content!.trim().length).toBeGreaterThan(10);
    });
  }
});

test.describe('Open Graph tags present', () => {
  for (const [path] of SEO_PAGES) {
    test(path, async ({ page }) => {
      await page.goto(`${BASE}${path}`);

      const ogTitle = await page
        .locator('meta[property="og:title"]')
        .getAttribute('content');
      expect(ogTitle, `og:title on ${path}`).toBeTruthy();

      const ogDescription = await page
        .locator('meta[property="og:description"]')
        .getAttribute('content');
      expect(ogDescription, `og:description on ${path}`).toBeTruthy();
    });
  }
});

test.describe('Canonical URL present', () => {
  for (const [path] of SEO_PAGES) {
    test(path, async ({ page }) => {
      await page.goto(`${BASE}${path}`);
      const canonical = await page
        .locator('link[rel="canonical"]')
        .getAttribute('href');
      expect(canonical, `canonical on ${path}`).toBeTruthy();
      expect(canonical).toMatch(/^https:\/\/vidra-ia\.com/);
    });
  }
});

test.describe('Hreflang ES/EN alternates', () => {
  /** Pages that have both ES and EN counterparts */
  const BILINGUAL_PAGES = [
    '/',
    '/who-we-are',
    '/services',
    '/blog',
    '/faq',
    '/contact',
  ];

  for (const path of BILINGUAL_PAGES) {
    test(path, async ({ page }) => {
      await page.goto(`${BASE}${path}`);

      const hreflangEs = await page
        .locator('link[rel="alternate"][hreflang="es"]')
        .getAttribute('href');
      expect(hreflangEs, `hreflang es on ${path}`).toBeTruthy();

      const hreflangEn = await page
        .locator('link[rel="alternate"][hreflang="en"]')
        .getAttribute('href');
      expect(hreflangEn, `hreflang en on ${path}`).toBeTruthy();
    });
  }
});

test.describe('FAQ structured data (schema.org)', () => {
  test('/faq has FAQPage JSON-LD', async ({ page }) => {
    await page.goto(`${BASE}/faq`);

    const jsonLd = await page.evaluate(() => {
      const scripts = Array.from(
        document.querySelectorAll('script[type="application/ld+json"]')
      );
      return scripts.map((s) => {
        try {
          return JSON.parse(s.textContent || '');
        } catch {
          return null;
        }
      });
    });

    const faqSchema = jsonLd.find(
      (s) => s && (s['@type'] === 'FAQPage' || s['@graph']?.some((n: any) => n['@type'] === 'FAQPage'))
    );
    expect(faqSchema, 'FAQPage JSON-LD not found on /faq').toBeTruthy();
  });

  test('/en/faq has FAQPage JSON-LD', async ({ page }) => {
    await page.goto(`${BASE}/en/faq`);

    const jsonLd = await page.evaluate(() => {
      const scripts = Array.from(
        document.querySelectorAll('script[type="application/ld+json"]')
      );
      return scripts.map((s) => {
        try {
          return JSON.parse(s.textContent || '');
        } catch {
          return null;
        }
      });
    });

    const faqSchema = jsonLd.find(
      (s) => s && (s['@type'] === 'FAQPage' || s['@graph']?.some((n: any) => n['@type'] === 'FAQPage'))
    );
    expect(faqSchema, 'FAQPage JSON-LD not found on /en/faq').toBeTruthy();
  });
});
