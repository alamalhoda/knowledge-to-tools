---
id: frontend-architecture-component-design
kind: architecture
domain: frontend
category: architecture
generated_at: 2026-06-11T20:40:16.250896+00:00
---

# Component Design

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
- Named slots 
