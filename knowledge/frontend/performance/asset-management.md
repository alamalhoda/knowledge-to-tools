---
title: Asset Management
summary: Asset management rules for images, fonts, icons including formats, responsive images, lazy loading, and caching strategies
domain: frontend
category: performance
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
priority: 50
kind: rule
---

# Asset Management Rules

## مدیریت بارگذاری تصاویر

### Formats
- از WebP برای تصاویر استفاده کن
- از AVIF برای تصاویر با کیفیت بالا استفاده کن
- از fallback formats استفاده کن

### Responsive Images
- از `srcset` استفاده کن
- از `sizes` استفاده کن
- از `picture` element استفاده کن

### Lazy Loading
- از native lazy loading استفاده کن
- از Intersection Observer استفاده کن
- از placeholder images استفاده کن

## مدیریت فونت‌ها

### Font Loading
- از font-display: swap استفاده کن
- از preload برای critical fonts استفاده کن
- از font subsetting استفاده کن

### Font Formats
- از WOFF2 استفاده کن
- از WOFF به عنوان fallback استفاده کن
- از system fonts در صورت امکان استفاده کن

## مدیریت آیکون‌ها

### SVG Icons
- از SVG برای آیکون‌ها استفاده کن
- از SVG sprite استفاده کن
- از icon components استفاده کن

### Icon Fonts
- از icon fonts برای آیکون‌های متعدد استفاده کن
- از subsetting استفاده کن
- از fallback استفاده کن

## قوانین

### Optimization
- از image optimization استفاده کن
- از compression استفاده کن
- برای این پروژه از CDN اینترنتی استفاده نکن؛ از نسخه محلی/آفلاین استفاده کن (ر.ک. `share/offline-no-cdn-policy.mdc`)

### Caching
- از proper cache headers استفاده کن
- از cache busting استفاده کن
- از versioning استفاده کن

### Loading Strategy
- از critical assets first استفاده کن
- از preload برای critical resources استفاده کن
- از prefetch برای future resources استفاده کن
