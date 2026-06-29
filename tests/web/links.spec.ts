import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';

/** Extract all internal href values from a selector scope */
async function collectInternalLinks(
  page: import('@playwright/test').Page,
  scope: string
): Promise<string[]> {
  return page.evaluate(
    ({ scope, base }) => {
      const container = document.querySelector(scope);
      if (!container) return [];
      return Array.from(container.querySelectorAll('a[href]'))
        .map((a) => (a as HTMLAnchorElement).href)
        .filter((href) => href.startsWith(base));
    },
    { scope, base: BASE }
  );
}

test.describe('Navbar links — no 404/500', () => {
  test('all navbar links respond successfully', async ({ page, request }) => {
    await page.goto(BASE);
    await page.waitForLoadState('networkidle');

    const links = await collectInternalLinks(page, 'nav, header');
    expect(links.length, 'No navbar links found').toBeGreaterThan(0);

    const unique = [...new Set(links)];
    const results = await Promise.all(
      unique.map(async (url) => {
        const res = await request.head(url, { maxRedirects: 5 });
        return { url, status: res.status() };
      })
    );

    const broken = results.filter((r) => r.status === 404 || r.status >= 500);
    expect(
      broken,
      `Broken navbar links: ${broken.map((r) => `${r.url} (${r.status})`).join(', ')}`
    ).toHaveLength(0);
  });
});

test.describe('Footer links — no 404/500', () => {
  test('all footer links respond successfully', async ({ page, request }) => {
    await page.goto(BASE);
    await page.waitForLoadState('networkidle');

    const links = await collectInternalLinks(page, 'footer');
    expect(links.length, 'No footer links found').toBeGreaterThan(0);

    const unique = [...new Set(links)];
    const results = await Promise.all(
      unique.map(async (url) => {
        const res = await request.head(url, { maxRedirects: 5 });
        return { url, status: res.status() };
      })
    );

    const broken = results.filter((r) => r.status === 404 || r.status >= 500);
    expect(
      broken,
      `Broken footer links: ${broken.map((r) => `${r.url} (${r.status})`).join(', ')}`
    ).toHaveLength(0);
  });
});

test.describe('Navbar links — EN version', () => {
  test('all navbar links on /en/ respond successfully', async ({
    page,
    request,
  }) => {
    await page.goto(`${BASE}/en/`);
    await page.waitForLoadState('networkidle');

    const links = await collectInternalLinks(page, 'nav, header');
    const unique = [...new Set(links)];

    const results = await Promise.all(
      unique.map(async (url) => {
        const res = await request.head(url, { maxRedirects: 5 });
        return { url, status: res.status() };
      })
    );

    const broken = results.filter((r) => r.status === 404 || r.status >= 500);
    expect(
      broken,
      `Broken EN navbar links: ${broken.map((r) => `${r.url} (${r.status})`).join(', ')}`
    ).toHaveLength(0);
  });
});
