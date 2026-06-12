---
id: frontend-state-local-vs-global
kind: skill
domain: frontend
category: state
generated_at: 2026-06-11T20:40:16.258675+00:00
---

# Local Vs Global

---
title: Local Vs Global
summary: Decision rules for choosing between local state and global state (Pinia) in Vue components
domain: frontend
category: state
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# Local vs Global State

## Decision Rule

State را در نزدیک‌ترین common ancestor نگه دار؛ اگر بیش از 2 کامپوننت به آن نیاز دارند از Pinia استفاده کن.

## Local State

**استفاده کن برای:**
- UI state که فقط یک component نیاز دارد (isOpen, isExpanded)
- Form inputs (local state تا submit)
- Temporary UI state

**مثال:** Modal open/close، dropdown state — با `ref` یا `reactive` در همان کامپوننت

## Global State (Pinia)

**استفاده کن برای:**
- Data که چندین component نیاز دارد
- User authentication state
- Application-wide settings
- Theme / locale
- Data مشترک بین views (مثلاً لیست خودروها، تنظیمات)

**قانون:** اگر بیش از 2 component به state نیاز دارند، در Pinia store تعریف کن.

