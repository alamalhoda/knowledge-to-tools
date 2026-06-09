---
id: frontend-patterns-props-events
kind: skill
domain: frontend
category: patterns
generated_at: 2026-06-09T20:12:15.487809+00:00
---

# Props Events

---
title: Props Events
summary: Vue props and emits guidelines (defineProps, defineEmits)
domain: frontend
category: patterns
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# Props and Emits (Vue 3)

## قوانین مدیریت Props

### Naming
- از camelCase در script استفاده کن
- در template می‌توانی kebab-case استفاده کن: `user-name`
- از boolean props با is/has/can شروع کن

### Types و Defaults
- از `defineProps` با type یا validator استفاده کن
- از default values برای optional props استفاده کن
- در .js از JSDoc برای type hint استفاده کن

✅ **Good:**
```vue
<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false },
  count: { type: Number, required: true }
});
</script>
```

### Organization
- props را به گروه‌های منطقی تقسیم کن
- از destructuring در صورت نیاز استفاده کن (با toRefs اگر reactive لازم است)

### Validation
- از validator در defineProps استفاده کن
- از clear error messages استفاده کن

## قوانین مدیریت Emits

### Naming
- از kebab-case برای event names در template استفاده کن: `@update-value`
- از action-oriented names استفاده کن

### Data
- از payload structure ثابت استفاده کن
- از minimal data استفاده کن

### Declaration
✅ **Good:**
```vue
<script setup>
const emit = defineEmits(['submit', 'cancel', 'update:modelValue']);
// با validation:
const emit = defineEmits({
  submit: (payload) => payload && typeof payload.id === 'number'
});
</scri
