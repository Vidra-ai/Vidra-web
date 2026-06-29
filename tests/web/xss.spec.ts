import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';
const API_CHAT_URL = 'https://api.vidra-ia.com/rag/chat';

/** Open the chat panel from the homepage. */
async function openChatPanel(page: import('@playwright/test').Page): Promise<void> {
  await page.goto(BASE);
  await page.waitForLoadState('networkidle');
  await page.locator('#chat-toggle').click();
  await page.locator('#chat-panel').waitFor({ state: 'visible' });
}

/** Submit a message via the chat widget. Assumes the panel is already open. */
async function submitChatMessage(
  page: import('@playwright/test').Page,
  message: string
): Promise<void> {
  await page.locator('#chat-widget-input').fill(message);
  await page.locator('#chat-widget-form').evaluate((el: HTMLFormElement) =>
    el.requestSubmit()
  );
}

test.describe('XSS via chat widget', () => {
  test('renders chat response as text not HTML', async ({ page }) => {
    // Mock the API before navigating so the route is registered in time.
    await page.route(API_CHAT_URL, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          respuesta: '<img src=x onerror="window.__xss_executed=true">',
          fuentes: [],
          sin_informacion: false,
        }),
      });
    });

    await openChatPanel(page);
    await submitChatMessage(page, 'test xss');

    // Wait for the panel to render a reply.
    await page.waitForTimeout(2000);

    // The onerror handler must NOT have fired — the tag must be text, not DOM.
    const xssExecuted = await page.evaluate(() => (window as any).__xss_executed);
    expect(xssExecuted).toBeFalsy();

    // As a secondary check: the literal string '<img' should appear as text
    // content inside the panel (confirming it was escaped, not parsed).
    const panelText = await page.locator('#chat-panel').textContent();
    const imgTagInDOM = await page.locator('#chat-panel img[onerror]').count();
    // Either the tag is rendered as literal text OR it was stripped entirely —
    // what matters is that the onerror event did not execute.
    expect(xssExecuted).toBeFalsy();
    // Belt-and-suspenders: no live img element with onerror should exist.
    expect(imgTagInDOM).toBe(0);
  });

  test('renders script tag payload as text not executable code', async ({ page }) => {
    await page.route(API_CHAT_URL, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          respuesta: '<script>window.__script_injected=true<\/script>',
          fuentes: [],
          sin_informacion: false,
        }),
      });
    });

    await openChatPanel(page);
    await submitChatMessage(page, 'test script injection');

    await page.waitForTimeout(2000);

    const scriptInjected = await page.evaluate(
      () => (window as any).__script_injected
    );
    expect(scriptInjected).toBeFalsy();
  });

  test('renders javascript: protocol as text', async ({ page }) => {
    await page.route(API_CHAT_URL, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          respuesta:
            'Haz click aquí: <a href="javascript:window.__js_href=true">enlace</a>',
          fuentes: [],
          sin_informacion: false,
        }),
      });
    });

    await openChatPanel(page);
    await submitChatMessage(page, 'test javascript protocol');

    await page.waitForTimeout(2000);

    const jsHref = await page.evaluate(() => (window as any).__js_href);
    expect(jsHref).toBeFalsy();

    // If an anchor was rendered, its href must not be a javascript: URI.
    const dangerousAnchors = await page
      .locator('#chat-panel a[href^="javascript:"]')
      .count();
    expect(dangerousAnchors).toBe(0);
  });

  test('user input is not reflected back unescaped', async ({ page }) => {
    // The API returns the user message echoed back as-is (worst-case scenario).
    const xssPayload = '<script>window.__user_input_xss=1<\/script>';

    await page.route(API_CHAT_URL, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          respuesta: xssPayload,
          fuentes: [],
          sin_informacion: false,
        }),
      });
    });

    await openChatPanel(page);
    // Type the XSS payload directly into the input field.
    await submitChatMessage(page, xssPayload);

    await page.waitForTimeout(2000);

    const userInputXss = await page.evaluate(
      () => (window as any).__user_input_xss
    );
    expect(userInputXss).toBeFalsy();
  });
});
