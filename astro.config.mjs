// @ts-check
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  site: "https://prismatic-labs.github.io",
  base: "/ldn-compute",
  // Keep whitespace in prose; compressHTML collapses "word </a> (note)" into "word</a>(note)".
  compressHTML: false,
  integrations: [react(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
