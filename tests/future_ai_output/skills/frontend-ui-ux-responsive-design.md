---
id: frontend-ui-ux-responsive-design
kind: skill
domain: frontend
category: ui-ux
generated_at: 2026-06-11T08:14:17.858986+00:00
---

# Responsive Design

---
title: Responsive Design
summary: Mobile-first responsive design principles, breakpoints, touch targets, responsive images, and CSS units
domain: frontend
category: ui-ux
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.css"
priority: 50
kind: skill
---

# Responsive Design

## Mobile-First Approach

طراحی از کوچک‌ترین صفحه (موبایل) شروع شود و به صفحات بزرگتر گسترش یابد.

**قانون:**
- Base styles بدون media query (موبایل)
- Media queries فقط برای min-width (scale up)
- از max-width استفاده نکن
- از progressive enhancement استفاده کن

## Breakpoints Strategy

```css
/* Base: 0-640px (mobile) - بدون media query */
.container {
  padding: 1rem;
  font-size: 16px;
}

/* sm: 640px+ (large mobile) */
@media (min-width: 640px) {
  .container {
    padding: 1.5rem;
  }
}

/* md: 768px+ (tablet) */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 18px;
  }
}

/* lg: 1024px+ (desktop) */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

**Breakpoints استاندارد:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Touch Targets

- حداقل 44×44px برای interactive elements
- Spacing کافی بین دکمه‌ها
- Thumb-friendly UI (دکمه‌های مهم در دسترس انگشت شست)

## Responsive Images

- استفاده از `srcset` با `sizes`
- WebP format با fallback
- `loading="lazy"` برای images off-screen
- `aspect-ratio` برای جلوگیری از layout shift

## CSS Units

- از viewport units استفاده ک
