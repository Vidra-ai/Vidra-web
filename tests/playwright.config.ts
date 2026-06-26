import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './web',
  timeout: 20000,
  retries: 1,
  workers: 2,
  reporter: [['html'], ['line']],
  use: {
    baseURL: 'https://vidra-ia.com',
    ignoreHTTPSErrors: false,
  },
});
