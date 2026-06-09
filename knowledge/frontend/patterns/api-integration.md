---
title: Api Integration
summary: Best practices for API integration, error handling, loading states, caching, and form validation
domain: frontend
category: patterns
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# API Integration Rules

## بهترین شیوه‌ها برای ارتباط با backend

### Service Layer
- از service layer برای API calls استفاده کن (مثلاً `src/services/`)
- از separation of concerns استفاده کن
- از error handling مناسب استفاده کن

### Error Handling
- از try-catch برای error handling استفاده کن
- از error messages واضح استفاده کن
- از error states در UI استفاده کن

### Loading States
- از loading states استفاده کن
- از skeleton screens استفاده کن
- از progress indicators استفاده کن

## مدیریت وضعیت‌های بارگذاری و خطا

### Loading States
- از boolean flags برای loading استفاده کن (مثلاً `isLoading`)
- از loading components استفاده کن
- از optimistic updates در صورت مناسب استفاده کن

### Error States
- از error messages واضح استفاده کن
- از retry mechanisms استفاده کن
- از error boundaries یا global error handler استفاده کن

### Empty States
- از empty states استفاده کن
- از helpful messages استفاده کن
- از call-to-action استفاده کن

## استراتژی caching داده‌ها

### Client-Side Caching
- از browser cache استفاده کن
- از memory cache (مثلاً در store) استفاده کن
- از cache invalidation استفاده کن

### Cache Strategy
- از cache-first برای static data استفاده کن
- از network-first برای dynamic data استفاده کن
- از stale-while-revalidate در صورت نیاز استفاده کن

## مدیریت فرم‌ها و اعتبارسنجی

### Form Validation
- از client-side validation استفاده کن
- از server-side validation استفاده کن
- از real-time validation استفاده کن

### Error Messages
- از error messages واضح استفاده کن
- از field-level errors استفاده کن
- از form-level errors استفاده کن

### User Experience
- از inline validation استفاده کن
- از helpful hints استفاده کن
- از disabled states استفاده کن
