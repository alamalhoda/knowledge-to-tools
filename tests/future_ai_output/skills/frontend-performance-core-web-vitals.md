---
id: frontend-performance-core-web-vitals
kind: skill
domain: frontend
category: performance
generated_at: 2026-06-11T08:14:17.856023+00:00
---

# Core Web Vitals

---
title: Core Web Vitals
summary: Core Web Vitals optimization guidelines for LCP, FID, and CLS performance metrics
domain: frontend
category: performance
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
priority: 50
kind: skill
---

# Core Web Vitals

## LCP (Largest Contentful Paint) <2.5s

**بهینه‌سازی:**
- Optimize largest image (hero image)
- Preload critical resources
- Reduce server response time

**تکنیک‌ها:**
- `fetchpriority="high"` برای hero image
- `<link rel="preload">` برای critical assets
- Image optimization (WebP, compression)

## FID (First Input Delay) <100ms

**بهینه‌سازی:**
- Reduce JavaScript execution time
- Code splitting
- Defer non-critical JavaScript
- Use `requestIdleCallback` برای non-critical tasks

**تکنیک‌ها:**
- Lazy load non-critical components
- Defer third-party scripts
- Reduce main thread blocking

## CLS (Cumulative Layout Shift) <0.1

**بهینه‌سازی:**
- Reserve space برای dynamic content
- Set dimensions برای images/videos
- Avoid inserting content above existing content
- Use `aspect-ratio` برای images

**تکنیک‌ها:**
- Skeleton screens با اندازه ثابت
- `aspect-ratio` CSS property
- Pre-calculate heights
- Font loading optimization

