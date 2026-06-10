---
id: frontend-core-code-quality
kind: reference
domain: frontend
category: core
generated_at: 2026-06-10T16:55:23.974633+00:00
---

# Code Quality

---
title: Code Quality
summary: Code quality standards, naming conventions, and documentation requirements for frontend (Vue 3, .vue, .js)
domain: frontend
category: core
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
priority: 50
kind: reference
---

# Code Quality Standards

## Shared Baseline

- baseline عمومی کیفیت کد در:
  `.cursor/rules/share/code-quality-baseline.mdc`
- این فایل فقط جزئیات اختصاصی frontend را تعریف می‌کند.

## Component Quality Checklist

- [ ] **Reusable:** کامپوننت قابل استفاده مجدد است؟
- [ ] **Props Typed:** props با JSDoc یا validator مستند شده؟
- [ ] **Emits:** custom emits مستند شده؟
- [ ] **Scoped Styles:** styles scoped هستند یا global conflicts ندارند؟
- [ ] **No Side Effects:** کامپوننت isolated و بدون side effects ناخواسته؟
- [ ] **Size:** کامپوننت کمتر از 200 خط؟

## قراردادهای نام‌گذاری

### فایل‌ها
- ✅ Components: **PascalCase** (`Button.vue`, `UserCard.vue`)
- ✅ Utilities: **camelCase** (`formatDate.js`, `validators.js`)
- ✅ Stores (Pinia): **camelCase** (`auth.js`, `vehicle.js`)
- ✅ Services: **camelCase** (`dashboardService.js`, `serviceTypeService.js`)
- ✅ Styles: **kebab-case** (`global.css`, `reset.css`)
- ✅ Constants: **UPPER_SNAKE_CASE** (`API_BASE_URL.js`, `COLORS.js`)

### متغیرها و توابع
- از camelCase برای متغیرها و توابع استفاده کن: `userName`, `getUserData()`
- از نام‌های توصیفی استفاده کن: `isLoading` به جای `loading`, `handleSubmit` به جای `submit`
- برای متغیرهای بولین، از
