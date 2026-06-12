---
id: frontend-architecture-project-structure
kind: architecture
domain: frontend
category: architecture
generated_at: 2026-06-11T20:40:16.251191+00:00
---

# Project Structure

---
title: Project Structure
summary: Project structure for frontend (Vue 3, Vite), file organization, naming, and asset management
domain: frontend
category: architecture
applies_to:
  - "frontend/**/*"
priority: 50
kind: architecture
---

# Project Structure (frontend)

## ساختار پیشنهادی

```
frontend/
├── public/                    # Static assets (بدون processing)
│   ├── favicon.ico
│   ├── fonts/                 # فونت‌های استاتیک
│   └── pwa-*.png
│
├── src/
│   ├── components/           # کامپوننت‌های قابل استفاده مجدد
│   │   ├── ui/               # کامپوننت‌های UI پایه (atoms, molecules)
│   │   ├── features/         # کامپوننت‌های feature-specific
│   │   ├── layout/           # layout (Sidebar, Header, MainLayout)
│   │   └── index.js          # barrel exports
│   │
│   ├── views/                # صفحات (route-level components)
│   │   ├── DashboardView.vue
│   │   ├── LoginView.vue
│   │   └── ...
│   │
│   ├── stores/               # Pinia stores (global state)
│   │   ├── auth.js
│   │   ├── vehicle.js
│   │   └── index.js
│   │
│   ├── services/             # API calls و business logic
│   │   ├── dashboardService.js
│   │   ├── serviceTypeService.js
│   │   └── index.js
│   │
│   ├── composables/          # Vue composables (useToast, useFocus, ...)
│   ├── router/               # Vue Router
│   │   └── index.js
│   ├── i18n/                 # بین‌المللی‌سازی
│   ├── locales/
│   ├── assets/               # منابع استاتیک (با Vite processing)
│   ├── style.css
