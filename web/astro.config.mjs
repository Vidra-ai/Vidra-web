// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';


export default defineConfig({
  site: 'https://vidra-ia.com',
  integrations: [
    sitemap({
      filter: (page) =>
        !page.includes('/search') &&
        !page.includes('/admin') &&
        !page.includes('/chat'),
      serialize(item) {
        item.lastmod = new Date().toISOString();
        const isRoot =
          item.url === 'https://vidra-ia.com/' ||
          item.url === 'https://vidra-ia.com/en/';
        const isBlogIndex =
          item.url === 'https://vidra-ia.com/blog/' ||
          item.url === 'https://vidra-ia.com/en/blog/';
        const isBlogPost = item.url.includes('/blog/') && !isBlogIndex;
        item.priority = isRoot ? 1.0 : 0.7;
        item.changefreq = isBlogPost ? 'never' : isBlogIndex ? 'weekly' : 'monthly';
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});