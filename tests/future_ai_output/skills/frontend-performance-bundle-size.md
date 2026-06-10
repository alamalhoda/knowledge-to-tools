---
id: frontend-performance-bundle-size
kind: rule
domain: frontend
category: performance
generated_at: 2026-06-10T16:55:23.976522+00:00
---

# Bundle Size

---
title: Bundle Size
summary: Bundle size management, performance budget constraints, code splitting, tree shaking, and bundle analysis
domain: frontend
category: performance
applies_to:
  - "frontend/src/**/*.js"
  - "frontend/vite.config.*"
priority: 50
kind: rule
---

# Bundle Size Management

## Performance Budget

**الزامات سخت:**
- Initial JS bundle: **<170KB** (gzipped)
- Initial CSS: **<50KB** (gzipped)
- Total page weight: **<1MB**

## Code Splitting

- Route-based code splitting (lazy load views)
- Component lazy loading برای components بزرگ
- Dynamic imports

**الگو:**
```javascript
const HeavyView = () => import('@/views/HeavyView.vue');
```

## Tree Shaking

- Import فقط آنچه نیاز است
- از `import *` پرهیز کن
- استفاده از named exports

## Bundle Analysis

- استفاده از bundle analyzer
- Track bundle size در CI/CD
- Alert هنگام exceed budget

