---
title: Runtime
summary: Runtime performance optimization including virtual scrolling, debouncing, throttling, requestAnimationFrame, and memoization
domain: frontend
category: performance
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# Runtime Performance

## Virtual Scrolling

برای لیست‌های بلند (10,000+ items):
- فقط visible items render کن
- Dynamic height calculation
- Smooth scrolling

## Debouncing & Throttling

- **Debounce:** برای search input (300ms delay)
- **Throttle:** برای scroll events (100ms interval)

## RequestAnimationFrame

برای animations:
- استفاده از `requestAnimationFrame` به جای `setTimeout`
- Smooth 60fps animations
- Cancel animation در cleanup

## Memoization

برای محاسبات سنگین:
- Cache results
- فقط recalculate هنگام dependency change
- از unnecessary recalculations پرهیز کن
- در Vue از `computed` استفاده کن

## Image Optimization

قوانین فرمت، lazy loading و `srcset` در
`knowledge/frontend/performance/asset-management.md`.

## Memory & Network

- از proper cleanup استفاده کن (event listener و subscription)
- از compression استفاده کن
- از HTTP/2 استفاده کن
