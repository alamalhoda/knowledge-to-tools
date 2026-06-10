---
id: frontend-tools-vue
kind: skill
domain: frontend
category: tools
generated_at: 2026-06-10T16:55:23.980159+00:00
---

# Vue

---
title: Vue
summary: Vue 3 best practices — script setup, Composition API, component structure, JSDoc for .js
domain: frontend
category: tools
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# Vue 3 Best Practices (frontend)

## &lt;script setup&gt;

- از `<script setup>` برای تمام کامپوننت‌های جدید استفاده کن
- ترتیب: imports → defineProps/defineEmits → composables/stores → state → computed → watch → lifecycle → methods

## Composition API

- از ref برای primitives و reference به object
- از reactive برای objectهایی که reassign نمی‌شوند
- از computed برای derived state
- از watch/watchEffect برای side effects

## Component Structure

- یک فایل یک کامپوننت؛ نام فایل PascalCase: `UserCard.vue`
- بخش‌ها به ترتیب: `<script setup>`, `<template>`, `<style scoped>`
- از scoped styles استفاده کن تا تداخل با global نباشد

## Props و Emits

- defineProps با type یا validator
- defineEmits با آرایه یا object (برای validation)
- در template از kebab-case برای events استفاده کن: `@update-value`

## JSDoc در .js (بدون TypeScript)

در فایل‌های .js (services، composables، utils) از JSDoc برای type hint استفاده کن:

```javascript
/**
 * @param {number} id
 * @returns {Promise<{ name: string }>}
 */
export async function fetchUser(id) { ... }
```

## Composables

- نام با پیشوند `use`: `useToast`, `useFocus`
- در پوشه `src/composables/` قرار بده
- state و logic قابل استفاده مجدد را برگردان

## Router و Views

- هر route به یک View component 
