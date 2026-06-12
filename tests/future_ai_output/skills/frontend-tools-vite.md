---
id: frontend-tools-vite
kind: skill
domain: frontend
category: tools
generated_at: 2026-06-11T20:40:16.259839+00:00
---

# Vite

---
title: Vite
summary: Vite configuration and optimization for frontend (Vue 3, Vue plugin)
domain: frontend
category: tools
applies_to:
  - "frontend/vite.config.*"
  - "frontend/package.json"
priority: 50
kind: skill
---

# Vite Configuration & Optimization (frontend)

## Base Configuration

```javascript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    cssMinify: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
        },
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'chunks/[name]-[hash].js',
        entryFileNames: '[name]-[hash].js',
      },
    },
    assetsInlineLimit: 4096,
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  envPrefix: 'VITE_',
});
```

## Code Splitting

**Lazy loading برای route components:**
```javascript
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/DashboardView.vue'),
  },
];
```

**قوانین:**
- از code splitting برای routes استفاده کن
- از tree shaking استفاده کن
- از minification استفاده کن

## Asset Optimization

- از proper asset imports استفاده کن
- از asset inl
