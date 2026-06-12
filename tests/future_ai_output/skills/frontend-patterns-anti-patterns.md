---
id: frontend-patterns-anti-patterns
kind: reference
domain: frontend
category: patterns
generated_at: 2026-06-11T20:40:16.254402+00:00
---

# Anti Patterns

---
title: Anti Patterns
summary: Common anti-patterns in frontend development and their correct solutions
domain: frontend
category: patterns
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: reference
---

# Anti-Patterns

قاعده‌های عمومی anti-pattern در
`.cursor/rules/share/code-quality-baseline.mdc`
تعریف شده‌اند. این فایل فقط anti-patternهای اختصاصی frontend را پوشش می‌دهد.

## Prop Drilling

❌ **Bad:** Prop drilling عمیق (>3 سطح)
- Props را از parent به child به grandchild می‌فرستی

✅ **Good:** استفاده از Pinia store
- Shared state در store نگه دار
- مستقیماً در کامپوننت‌ها با store استفاده کن

## Massive Components

❌ **Bad:** کامپوننت 500+ خطی
- همه چیز در یک فایل

✅ **Good:** تقسیم به کامپوننت‌های کوچک
- Single Responsibility Principle
- Composable components

## Inline Styles Everywhere

❌ **Bad:** استفاده زیاد از inline styles
- Hard to maintain
- No reusability

✅ **Good:** Scoped styles
- `<style scoped>` یا CSS classes
- CSS Custom Properties

## No Loading States

❌ **Bad:** بدون loading indicator
- کاربر منتظر می‌ماند بدون feedback

✅ **Good:** Loading states
- Spinner یا skeleton screen
- Clear feedback

## Global State Abuse

❌ **Bad:** همه چیز در Pinia store
- UI states که فقط local باید باشند

✅ **Good:** Local state برای UI
- Pinia فقط برای shared data
- ref/reactive در component برای UI-specific state

