---
title: Accessibility
summary: WCAG 2.1 AA accessibility guidelines, semantic HTML, ARIA attributes, keyboard navigation, and screen reader support
domain: frontend
category: ui-ux
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
priority: 50
kind: rule
---

# Accessibility (WCAG 2.1 AA)

## Semantic HTML

همیشه از درست‌ترین HTML element استفاده کن.

❌ **Bad:** `<div class="button">`
✅ **Good:** `<button>`

❌ **Bad:** `<div class="heading">`
✅ **Good:** `<h1>`

**ساختار معنایی:**
- `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`
- `<section>` برای بخش‌های منطقی
- لیست‌ها: `<ul>`, `<ol>`, `<dl>`
- از heading hierarchy صحیح استفاده کن (h1 → h2 → h3)
- از landmarks (header, nav, main, footer) استفاده کن

## ARIA Attributes

**قانون:** "No ARIA is better than bad ARIA"

فقط زمانی استفاده کن که semantic HTML کافی نیست:
- Custom widgets
- Dynamic content
- Complex interactions

**مثال‌های درست:**
- `aria-expanded` برای dropdown
- `aria-label` برای icon buttons
- `aria-describedby` برای help text
- `aria-live` برای dynamic updates
- از `aria-hidden` برای محتوای تزئینی استفاده کن

## Keyboard Navigation

**الزامات:**
- Tab: حرکت به جلو
- Shift+Tab: حرکت به عقب
- Enter/Space: فعال‌سازی
- Escape: بستن modal/dropdown
- Arrow keys: حرکت در لیست‌ها/منوها

**Focus Management:**
- همه interactive elements باید keyboard-accessible باشند
- Focus indicators واضح و قابل مشاهده
- Focus trap در modal ها
- Skip links برای navigation

## Color Contrast

**الزامات WCAG 2.1 AA:**
- Text: حداقل 4.5:1
- Large text (18pt+): حداقل 3:1
- UI Components: حداقل 3:1

❌ **Bad:** `#ddd` on `#aaa` (1.5:1)
✅ **Good:** `#ffffff` on `#3b82f6` (8.6:1)

## Screen Reader Support

- همه images دارای alt text مناسب
- Form inputs دارای label یا aria-label
- با screen reader تست شده
- Live regions برای dynamic content
- Descriptive link text (نه "click here")

## Reduced Motion

- از `prefers-reduced-motion` media query استفاده کن
- از animations غیرضروری پرهیز کن

## Accessibility Checklist

- [ ] Semantic HTML استفاده شده؟
- [ ] همه interactive elements با keyboard قابل دسترسی؟
- [ ] Focus indicators واضح هستند؟
- [ ] Color contrast حداقل 4.5:1 است؟
- [ ] Screen reader tested شده؟
- [ ] ARIA attributes مناسب استفاده شده؟
- [ ] Reduced motion respected شده؟
