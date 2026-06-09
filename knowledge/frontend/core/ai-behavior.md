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
   - بهینه‌سازی‌ها را بر اساس داده‌های واقعی انجام ده، نه حدس و گمان
   - محدودیت‌های دستگاه‌های ضعیف‌تر را در نظر بگیر

5. **Maintainability** - قابلیت نگهداری
   - کدی بنویس که همکار بعدی بتواند به راحتی آن را درک و تغییر دهد
   - از ساختارهای پیچیده و "هوشمندانه" بدون دلیل مشخص پرهیز کن
   - کامپوننت‌ها باید قابل استفاده مجدد و مستقل باشند

## قوانین خاص تولید کد Frontend توسط AI

- **همیشه Responsive بساز:** هر کامپوننت باید در تمام breakpoints تست شود
- **Component Reusability:** کامپوننت‌ها باید قابل استفاده مجدد و isolated باشند
- **Props با Type Safety:** همه props باید type-safe باشند (JSDoc یا TypeScript)
- **همیشه قبل از معرفی یک الگوی پیچیده، توضیح بده** چرا این الگو لازم است
- **تجربه کاربری را فدای کد "تمیز" نکن** - گاهی یک راه‌حل ساده‌تر برای کاربر بهتر است حتی اگر کد کمی پیچیده‌تر شود
- **در صورت شک، از کاربر بپرس:** برای طراحی UI پیچیده، mockup یا توضیح بیشتر بخواه
- **همیشه به دسترس‌پذیری (Accessibility) توجه کن** - این یک ویژگی اضافی نیست، یک الزام است
- **تغییرات تدریجی را به تغییرات بزرگ ترجیح بده** (Incremental Refactoring)

## Performance Budget (بودجه عملکرد)

**الزامات سخت:**
- Initial JS bundle: **<170KB** (gzipped)
- Initial CSS: **<50KB** (gzipped)
- Total page weight: **<1MB**
- Images: WebP format, lazy-loaded
- Fonts: <100KB, with font-display: swap

**Core Web Vitals:**
- **LCP (Largest Contentful Paint):** <2.5s
- **FID (First Input Delay):** <100ms
- **CLS (Cumulative Layout Shift):** <0.1

## قوانین تصمیم‌گیری برای AI

1. **اولویت تجربه کاربری:** همیشه تجربه کاربری را بر کد "تمیز" ترجیح ده
2. **دسترس‌پذیری اولیه:** دسترس‌پذیری یک ویژگی اضافی نیست، یک الزام است
3. **عملکرد مهم است:** بهینه‌سازی‌ها را بر اساس داده‌های واقعی انجام ده، نه حدس و گمان
4. **سادگی بر پیچیدگی:** راه‌حل ساده را به راه‌حل پیچیده ترجیح ده، مگر اینکه دلیل محکمی برای پیچیدگی وجود داشته باشد
5. **توسعه تدریجی:** تغییرات بزرگ را به بخش‌های کوچکتر تقسیم کنید
6. **ثبات در طراحی:** از design tokens و اصول طراحی ثابت استفاده کنید
7. **واکنش‌گرایی اول:** برای موبایل طراحی کنید، سپس برای صفحات بزرگتر

## الگوهای ترجیحی برای AI

1. **Component-First Development:** همیشه از کامپوننت‌های قابل استفاده مجدد استفاده کنید
2. **Atomic Design:** از اصول Atomic Design برای ساختار UI استفاده کنید
3. **State Management:** از Pinia برای state سراسری استفاده کنید
4. **Error Handling:** از proper error handling و loading states استفاده کنید
5. **Responsive Design:** از رویکرد mobile-first برای طراحی واکنش‌گرا استفاده کنید
6. **Accessibility:** از proper ARIA attributes و semantic HTML استفاده کنید
7. **Performance:** از lazy loading و code splitting برای بهینه‌سازی عملکرد استفاده کنید

## User Experience Over Developer Experience

وقتی تجربه کاربر و راحتی توسعه‌دهنده در تضاد هستند، تجربه کاربر برنده است.

مثال:
- Bundle size optimization (حتی اگر کد پیچیده‌تر شود)
- Manual performance optimization (حتی اگر زمان بیشتری بگیرد)
- Accessibility compliance (حتی اگر markup بیشتری لازم باشد)
