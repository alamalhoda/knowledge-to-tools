---
id: frontend-core-ai-behavior
kind: rule
domain: frontend
category: core
generated_at: 2026-06-09T20:12:15.483109+00:00
---

# Ai Behavior

---
title: Ai Behavior
summary: AI behavior guidelines and priorities for frontend development
domain: frontend
category: core
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
priority: 50
kind: rule
---

# AI Behavior Guidelines

## اولویت‌های اجرایی (به ترتیب اهمیت)

1. **UI/UX First** - تجربه کاربر در اولویت
   - کد باید تجربه کاربری روان و بصری جذاب ایجاد کند
   - هر کامپوننت باید responsive و accessible باشد
   - رابط کاربری باید intuitive و self-explanatory باشد
   - از اصول طراحی بصری پیروی کن (visual hierarchy, contrast, spacing)
   - همیشه از دید کاربر نهایی به طراحی نگاه کن
   - تاخیر در واکنش‌ها را به حداقل برسان

2. **Accessibility First** - دسترسی‌پذیری در اولویت
   - WCAG 2.1 AA compliance الزامی است
   - همیشه از semantic HTML استفاده کن
   - keyboard navigation و screen reader support اجباری
   - Color contrast minimums را رعایت کن (4.5:1 for text)
   - دسترس‌پذیری یک ویژگی اضافی نیست، یک الزام است

3. **Mobile-First** - موبایل در اولویت
   - طراحی از موبایل شروع شود و به دسکتاپ گسترش یابد
   - Touch targets حداقل 44×44px
   - از viewport units و relative units استفاده کن (نه px ثابت)
   - برای موبایل طراحی کن، سپس برای صفحات بزرگتر

4. **Performance First** - عملکرد در اولویت
   - Bundle size: هر route حداکثر 170KB (gzipped)
   - First Contentful Paint: <1.8s
   - Time to Interactive: <3.8s
   - از lazy loading و code splitting استفاده کن
   - برنامه باید سریع بارگذاری شود و روان اجرا شود
   - بهینه‌سازی‌ها را بر 
