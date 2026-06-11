---
id: frontend-ui-ux-user-feedback
kind: skill
domain: frontend
category: ui-ux
generated_at: 2026-06-11T08:14:17.859601+00:00
---

# User Feedback

---
title: User Feedback
summary: User feedback patterns including loading states, error handling, success feedback, skeleton screens, and toast notifications
domain: frontend
category: ui-ux
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# User Feedback

## Loading States

همیشه loading indicator برای async operations نمایش بده.

**الگوها:**
- Spinner برای عملیات کوتاه
- Skeleton screens برای محتوای در حال بارگذاری
- Progress bar برای عملیات طولانی

❌ **Bad:** کاربر منتظر می‌ماند بدون feedback
✅ **Good:** Loading indicator واضح

## Error Handling

- پیام‌های خطا واضح و مفید
- راه حل یا action بعدی پیشنهاد بده
- Dismissible error messages
- Error recovery options

## Success Feedback

- بازخورد موفقیت برای actions مهم
- Toast notifications برای actions سریع
- Visual confirmation (checkmark, animation)

## Skeleton Screens

بهتر از spinners برای محتوای در حال بارگذاری:
- ساختار صفحه را نشان می‌دهد
- Perceived performance بهتر
- کاهش layout shift

## Toast Notifications

برای بازخورد سریع:
- Auto-dismiss بعد از 3-5 ثانیه
- Manual dismiss option
- Multiple toasts stack
- Different types: info, success, warning, error

