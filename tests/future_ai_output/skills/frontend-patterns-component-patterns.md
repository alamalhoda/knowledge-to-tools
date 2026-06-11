---
id: frontend-patterns-component-patterns
kind: skill
domain: frontend
category: patterns
generated_at: 2026-06-11T08:14:17.854922+00:00
---

# Component Patterns

---
title: Component Patterns
summary: Vue 3 component structure, script setup order, and standard patterns
domain: frontend
category: patterns
applies_to:
  - "frontend/src/**/*.vue"
priority: 50
kind: skill
---

# Component Patterns (Vue 3)

## Component Structure با &lt;script setup&gt;

**ترتیب استاندارد در &lt;script setup&gt;:**
1. Imports
2. defineProps / defineEmits
3. Composables (استفاده از store، router، composables دیگر)
4. Local state (ref, reactive)
5. computed
6. watch / watchEffect
7. Lifecycle (onMounted, onUnmounted, ...)
8. Event handlers و helper functions

✅ **Good:**
```vue
<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({ ... });
const emit = defineEmits(['submit']);

const count = ref(0);
const doubled = computed(() => count.value * 2);

onMounted(() => { ... });

function handleSubmit() { ... }
</script>

<template>...</template>

<style scoped>...</style>
```

## Props و Emits Pattern

- از defineProps با type یا validator استفاده کن
- از defineEmits برای events استفاده کن
- Props و emits را در بالای script قرار بده

## Slots Pattern

- Default slot برای محتوای اصلی
- Named slots برای بخش‌های خاص
- Slot fallback با محتوای پیش‌فرض

## استفاده از Pinia در کامپوننت

- از store فقط در جایی که نیاز است استفاده کن
- برای نگه داشتن reactivity از `storeToRefs(store)` استفاده کن؛ actions را مستقیم از store صدا بزن

