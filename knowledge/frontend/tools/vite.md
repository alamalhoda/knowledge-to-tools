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
- از asset inlining برای فایل‌های کوچک (<4KB) استفاده کن

## بهینه‌سازی

### Configuration
- از path alias (`@` → `src/`) استفاده کن
- از environment variables با پیشوند `VITE_` استفاده کن

### Development
- از HMR استفاده کن
- از dev server proxy برای API استفاده کن

### Production
- از chunk splitting برای vendor (vue, vue-router, pinia) استفاده کن
- از build optimization استفاده کن
