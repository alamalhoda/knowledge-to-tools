---
id: frontend-ui-ux-styling
kind: reference
domain: frontend
category: ui-ux
generated_at: 2026-06-11T08:14:17.859286+00:00
---

# Styling

---
title: Styling
summary: Styling strategy, scoped CSS, theme management, design tokens, and BEM naming conventions
domain: frontend
category: ui-ux
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.css"
priority: 50
kind: reference
---

# Styling Strategy

## رویکرد پیشنهادی

### Scoped CSS
- از `<style scoped>` در کامپوننت‌های Vue استفاده کن
- تداخل استایل‌ها را به حداقل می‌رساند

### Global CSS
- برای متغیرهای CSS (مثلاً در `style.css`)
- برای reset styles
- برای استایل‌های پایه

## مدیریت تم‌ها

### CSS Variables
- از CSS variables برای تم‌ها استفاده کن
- از `:root` برای variables سراسری استفاده کن
- از `[data-theme]` برای تم‌های مختلف استفاده کن

### Light/Dark Mode
- از `prefers-color-scheme` استفاده کن
- از toggle برای تغییر تم استفاده کن
- از CSS variables برای رنگ‌ها استفاده کن

## Design Tokens

### Colors
- از semantic color names استفاده کن
- از color palette ثابت استفاده کن

### Spacing
- از spacing scale استفاده کن
- از consistent spacing استفاده کن

### Typography
- از typography scale استفاده کن
- از font weights مناسب استفاده کن

## قوانین

- از BEM naming استفاده کن
- از utility classes محدود استفاده کن (مثلاً Tailwind در frontend)
- از CSS variables برای مقادیر استفاده کن
- از responsive units استفاده کن

