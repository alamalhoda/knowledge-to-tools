---
title: Meta Principles
summary: Meta-principles and fundamental design principles underlying all frontend development rules
domain: frontend
category: core
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
priority: 50
kind: principle
---

# Meta-Principles

اصول پایه frontend. اصول جهان‌شمول در فایل اشتراکی تعریف شده‌اند:
`knowledge/shared/engineering-principles.md`

اگر اختلافی وجود داشت، rule تخصصی frontend در این فایل اولویت دارد.

## Frontend-Specific Principles

### Single Source of Truth در UI
- برای تصمیم‌های طراحی از design tokens و CSS variables استفاده کن.
- منبع مقادیر design باید مرکزی و قابل ردیابی باشد.

### Component Reusability
- کامپوننت‌ها isolated و self-contained باشند.
- از props/slots برای customization استفاده کن.
- وابستگی مستقیم به context خاص parent ایجاد نکن.

### Progressive Enhancement
- HTML/CSS پایه باید بدون JavaScript نیز قابل استفاده باشد.
- فرم‌ها باید با HTML5 validation کار کنند.

### Mobile-First Design
جزئیات breakpoints، touch targets و CSS units در
`knowledge/frontend/ui-ux/responsive-design.md`.

### Accessibility First
- semantic HTML همیشه اولویت دارد.
- ARIA فقط وقتی semantic کافی نیست استفاده شود.
- همه عناصر تعاملی باید keyboard-accessible باشند.
جزئیات WCAG در `knowledge/frontend/ui-ux/accessibility.md`.

### Performance First (Frontend)
بودجه bundle در `knowledge/frontend/performance/bundle-size.md`.
متریک‌های LCP/FID/CLS در `knowledge/frontend/performance/core-web-vitals.md`.
