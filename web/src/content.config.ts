import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({
    pattern: '**/*.{md,mdx}',
    base: './src/content/blog',
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    lang: z.enum(['es', 'en']),
    category: z.enum(['analytics', 'machine-learning', 'deep-learning', 'empresa']),
    translationKey: z.string().optional(),
    image: z.string().optional(),
    noindex: z.boolean().optional(),
  }),
});

export const collections = { blog };