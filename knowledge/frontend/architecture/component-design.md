---
title: Component Design
summary: Vue component design principles, props, emits, slots, and composition
domain: frontend
category: architecture
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: architecture
---

# Component Design Principles (Vue 3)

## اصول طراحی کامپوننت

### Single Responsibility Principle (SRP)

هر کامپوننت فقط یک کار انجام دهد.

**Code Smell:**
- کامپوننت‌های بیش از 200 خط
- کامپوننت‌هایی که هم state management و هم UI rendering دارند
- نام‌های ترکیبی: `UserProfileFormWithValidation`

**اصل:** تقسیم به کامپوننت‌های کوچک‌تر با مسئولیت واحد

### Composition over Configuration

- از composition برای ترکیب قابلیت‌ها استفاده کن
- از slots برای محتوای پویا استفاده کن
- از props برای configuration استفاده کن

### Props Design

جزئیات `defineProps`، types، defaults و validation در
`knowledge/frontend/patterns/props-events.md`.

### Emits Design

جزئیات `defineEmits`، naming و payload در
`knowledge/frontend/patterns/props-events.md`.

### Slots Pattern

- Default slot برای محتوای اصلی
- Named slots برای بخش‌های خاص
- Slot fallback با محتوای پیش‌فرض

## Props Down, Events Up

داده از parent به child با props؛ communication از child به parent با emit.

**قانون:**
- State در parent (یا Pinia) نگه دار
- Child فقط props می‌گیرد و emit می‌کند
- از direct mutation از بیرون در child پرهیز کن

## Reusability

- کامپوننت‌ها باید قابل استفاده مجدد باشند
- از props برای customization استفاده کن
- از slots برای flexibility استفاده کن
- هر کامپوننت باید بدون وابستگی به parent/context خاص کار کند

## Documentation

- از JSDoc برای props در composables/services استفاده کن
- از comments برای منطق پیچیده استفاده کن
- File header در صورت نیاز (توضیح فارسی)
- Emits مستند شده

## Atomic Design در frontend

سلسله‌مراتب atoms/molecules/organisms در
`knowledge/frontend/architecture/atomic-design.md`.
ساختار پوشه `components/` در
`knowledge/frontend/architecture/project-structure.md`.
