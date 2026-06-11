---
id: frontend-ui-ux-interaction-patterns
kind: skill
domain: frontend
category: ui-ux
generated_at: 2026-06-11T08:14:17.858640+00:00
---

# Interaction Patterns

---
title: Interaction Patterns
summary: Interaction patterns including form validation, optimistic UI updates, debouncing, throttling, animations, and modal patterns
domain: frontend
category: ui-ux
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# Interaction Patterns

## Form Validation

**Real-time validation:**
- Validation بعد از blur
- Show errors فقط برای fields touched
- Clear errors هنگام تایپ
- HTML5 validation به عنوان fallback

**الگو:**
1. User types
2. User blurs field
3. Show validation errors
4. Clear errors on next input
5. Submit validation (all fields)

## Optimistic UI Updates

برای UX بهتر:
1. UI را فوری update کن
2. در background request بفرست
3. در صورت خطا، rollback کن

**مثال:** Like button, Delete item

## Debouncing & Throttling

- **Debounce:** برای search input (بعد از توقف تایپ)
- **Throttle:** برای scroll events (حداکثر هر X میلی‌ثانیه)

## Animation Principles

- Subtle animations (150-300ms)
- Easing functions طبیعی
- Reduce motion برای accessibility
- `prefers-reduced-motion` را respect کن

## Modal & Dialog Patterns

- Focus trap در modal
- Escape key برای بستن
- Click outside برای بستن (optional)
- ARIA attributes (`aria-modal`, `aria-labelledby`)
- Focus return بعد از بستن

