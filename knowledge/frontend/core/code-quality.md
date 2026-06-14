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
  `knowledge/shared/code-quality-baseline.md`
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
- برای متغیرهای بولین، از پیشوندهای is/has/can استفاده کن: `isVisible`, `hasError`, `canEdit`

### CSS
- از BEM (Block Element Modifier) استفاده کن: `.card__title--highlighted`
- از kebab-case برای نام کلاس‌ها استفاده کن: `.user-profile`, `.search-box`
- از پیشوندهای خاص برای جلوگیری از تداخل: `.c-button` (c برای component), `.u-hidden` (u برای utility)

### کامپوننت‌ها
- از نام‌های توصیفی استفاده کن: `UserProfile` به جای `User`, `SearchBox` به جای `Search`
- برای کامپوننت‌های UI پایه: `Button.vue`, `Input.vue`, `Modal.vue`
- برای کامپوننت‌های feature: `UserCard.vue`, `ServiceTypeSelector.vue`

## Code Smells

**کامپوننت‌های مشکوک:**
- کامپوننت‌های بیش از 200 خط
- کامپوننت‌هایی که هم state management و هم UI rendering دارند
- نام‌های ترکیبی: `UserProfileFormWithValidation`

## Documentation Requirements

هر کامپوننت باید شامل:
- File header (توضیح فارسی در صورت نیاز)
- Props مستند شده (JSDoc یا defineProps با type)
- Emits مستند شده
- نحوه استفاده
