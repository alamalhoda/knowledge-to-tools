---
id: frontend-ui-ux-accessibility
kind: rule
domain: frontend
category: ui-ux
generated_at: 2026-06-11T20:40:16.260345+00:00
---

# Accessibility

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

## Color
