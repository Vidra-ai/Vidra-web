import { test, expect } from '@playwright/test';

const BASE = 'https://vidra-ia.com';
const API_CHAT_URL = 'https://api.vidra-ia.com/rag/chat';

test.describe('Chat widget — end to end', () => {
  test('toggle button is visible on homepage', async ({ page }) => {
    await page.goto(BASE);
    await page.waitForLoadState('networkidle');

    const toggle = page.locator('#chat-toggle');
    await expect(toggle).toBeVisible();
  });

  test('clicking toggle opens the chat panel', async ({ page }) => {
    await page.goto(BASE);
    await page.waitForLoadState('networkidle');

    const toggle = page.locator('#chat-toggle');
    const panel = page.locator('#chat-panel');

    // Panel should be hidden before interaction
    await expect(panel).not.toBeVisible();

    await toggle.click();
    await expect(panel).toBeVisible();
  });

  test('chat panel contains input and form', async ({ page }) => {
    await page.goto(BASE);
    await page.waitForLoadState('networkidle');

    await page.locator('#chat-toggle').click();
    await page.locator('#chat-panel').waitFor({ state: 'visible' });

    await expect(page.locator('#chat-widget-input')).toBeVisible();
    await expect(page.locator('#chat-widget-form')).toBeVisible();
  });

  test('sends a message and receives a response from the API', async ({ page }) => {
    await page.goto(BASE);
    await page.waitForLoadState('networkidle');

    // Open the chat panel
    await page.locator('#chat-toggle').click();
    await page.locator('#chat-panel').waitFor({ state: 'visible' });

    const input = page.locator('#chat-widget-input');
    const form = page.locator('#chat-widget-form');

    // Intercept the API call to verify it's made correctly
    const apiResponsePromise = page.waitForResponse(
      (response) =>
        response.url().startsWith(API_CHAT_URL) && response.status() < 500,
      { timeout: 15000 }
    );

    await input.fill('¿Qué servicios ofrece VIDRA?');
    await form.evaluate((el: HTMLFormElement) => el.requestSubmit());

    const apiResponse = await apiResponsePromise;
    expect(apiResponse.status(), 'API responded with error').toBeLessThan(400);

    // Wait for the widget to render a reply (any new text node in the panel)
    await page.waitForFunction(
      () => {
        const panel = document.querySelector('#chat-panel');
        if (!panel) return false;
        const text = panel.textContent || '';
        // At least one assistant message should appear after the user message
        return text.length > 50;
      },
      { timeout: 15000 }
    );
  });

  test('chat widget present on a non-home page (/contact)', async ({ page }) => {
    await page.goto(`${BASE}/contact`);
    await page.waitForLoadState('networkidle');

    await expect(page.locator('#chat-toggle')).toBeVisible();
  });
});
