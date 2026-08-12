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
`knowledge/shared/code-quality-baseline.md`
تعریف شده‌اند. این فایل فقط anti-patternهای اختصاصی frontend را پوشش می‌دهد.

## Prop Drilling

❌ **Bad:** Prop drilling عمیق (>3 سطح)

✅ **Good:** shared state را در Pinia نگه دار. قانون تصمیم local vs global در
`knowledge/frontend/state/local-vs-global.md`.

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

✅ **Good:** Spinner، skeleton یا toast. الگوها در
`knowledge/frontend/ui-ux/user-feedback.md`.

## Global State Abuse

❌ **Bad:** همه چیز در Pinia store (از جمله UI state محلی)

✅ **Good:** local state برای UI؛ Pinia فقط برای دادهٔ مشترک. قانون تصمیم در
`knowledge/frontend/state/local-vs-global.md`.
