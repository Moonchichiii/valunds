import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwind from "@tailwindcss/vite";
import compression from "vite-plugin-compression";
import { ViteImageOptimizer } from "vite-plugin-image-optimizer";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig({
  // If your .env files live at repo root, uncomment:
  // envDir: "..",

  publicDir: "public",

  plugins: [
    react(),
    tailwind(),

    // Dual compression: brotli + gzip (keeps originals)
    compression({ algorithm: "brotliCompress", ext: ".br", threshold: 10_240, deleteOriginFile: false }),
    compression({ algorithm: "gzip",           ext: ".gz", threshold: 10_240, deleteOriginFile: false }),

    // Lossy but reasonable defaults; easily tuned later
    ViteImageOptimizer({
      png:  { quality: 80 },
      jpeg: { quality: 80 },
      jpg:  { quality: 80 },
      webp: { quality: 80 },
      avif: { quality: 50 },
      exclude: /favicon|apple-touch-icon/i,
    }),
  ],

  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
      "@/components": resolve(__dirname, "src/components"),
      "@/features":   resolve(__dirname, "src/features"),
      "@/lib":        resolve(__dirname, "src/lib"),
      "@/i18n":       resolve(__dirname, "src/i18n"),
      "@/pages":      resolve(__dirname, "src/pages"),
      "@/api":        resolve(__dirname, "src/api"),
    },
    // keep this small to avoid extra fs checks during resolve (perf)
    extensions: [".tsx", ".ts", ".jsx", ".js"],
  },

  // Keep dev snappy; drop debug stuff only in prod builds
  esbuild: {
    legalComments: "none",
    logOverride: { "this-is-undefined-in-esm": "silent" },
    drop: process.env.NODE_ENV === "production" ? ["console", "debugger"] : [],
  },

  build: {
    target: "es2020",
    minify: "esbuild",
    cssCodeSplit: true,
    sourcemap: false,
    chunkSizeWarningLimit: 500,
    copyPublicDir: true,
    rollupOptions: {
      output: {
        // sensible vendor chunking for your stack
        manualChunks: {
          "react-vendor": ["react", "react-dom", "react/jsx-runtime"],
          "router": ["@tanstack/react-router"],
          "query": ["@tanstack/react-query"],
          "motion": ["framer-motion"],
          "i18n": ["i18next", "react-i18next"],
        },
        entryFileNames: "assets/[name]-[hash].js",
        chunkFileNames: "assets/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          const rootAssets = new Set([
            "favicon.ico",
            "robots.txt",
            "site.webmanifest",
            "apple-touch-icon.png",
            "og-image-1200x630.jpg",
          ]);
          return assetInfo.name && rootAssets.has(assetInfo.name)
            ? "[name][extname]"
            : "assets/[name]-[hash][extname]";
        },
      },
    },
    // CommonJS interop safety
    commonjsOptions: {
      include: [/node_modules/],
      transformMixedEsModules: true,
    },
  },

  // Pre-bundle some hot deps to avoid waterfalls on first load
  optimizeDeps: {
    include: [
      "react",
      "react-dom",
      "@tanstack/react-router",
      "@tanstack/react-query",
      "axios",
      "framer-motion",
      "i18next",
      "react-i18next",
      "date-fns",
      "lucide-react",
    ],
  },

  // Warm up frequently used graph nodes for faster first paint
  server: {
    host: true,
    port: 5173,
    strictPort: false,
    warmup: {
      clientFiles: ["./index.html", "./src/main.tsx"],
    },
  },

  preview: {
    host: true,
    port: 5173,
    strictPort: false,
  },
});
