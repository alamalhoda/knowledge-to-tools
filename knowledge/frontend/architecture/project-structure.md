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
│   ├── style.css             # استایل سراسری
│   ├── main.js               # Entry point
│   └── App.vue
│
├── src/test/                 # Test setup و utils
├── .env.example
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## قوانین سازماندهی

- هر کامپوننت در فایل خودش
- از index.js برای barrel export استفاده کن
- از grouping منطقی استفاده کن (ui/, features/, layout/)
- از naming conventions ثابت استفاده کن

## نامگذاری فایل‌ها

- ✅ Components: **PascalCase** (`Button.vue`, `UserCard.vue`)
- ✅ Utilities/Services: **camelCase** (`formatDate.js`, `serviceTypeService.js`)
- ✅ Stores (Pinia): **camelCase** (`auth.js`, `vehicle.js`)
- ✅ Styles: **kebab-case** (`global.css`, `reset.css`)

## مدیریت Assets

### تصاویر
- در `public/` یا `src/assets/` قرار بده
- از فرمت‌های مناسب استفاده کن (JPG, PNG, SVG, WebP)
- از responsive images با `srcset` استفاده کن

### فونت‌ها
- در `public/fonts` یا `src/assets/fonts` قرار بده
- از فرمت‌های WOFF2 و WOFF استفاده کن

### آیکون‌ها
- از SVG استفاده کن
- در `src/assets/` یا کامپوننت‌های Icon
