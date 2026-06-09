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

- از `defineProps` با type یا validator استفاده کن
- از default values مناسب استفاده کن
- در .js از JSDoc برای type hint استفاده کن
- Props مستند شده

✅ **Good (script setup):**
```vue
<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false }
});
</script>
```

### Emits Design

- از `defineEmits` برای custom events استفاده کن
- از event names واضح (kebab-case در template) استفاده کن
- از payload structure ثابت استفاده کن

✅ **Good:**
```vue
<script setup>
const emit = defineEmits(['submit', 'cancel']);
emit('submit', { id: 1, name: 'Ali' });
</script>
```

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

**ساختار:**
```
components/
├── ui/           # atoms & molecules
│   ├── Button.vue
│   ├── Input.vue
│   ├── Card.vue
│   └── Modal.vue
├── features/     # feature-specific
├── layout/       # MainLayout, Sidebar, Header
```

**قانون:** کامپوننت‌های کوچک را بساز و با composition ترکیب کن
