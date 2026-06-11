---
id: frontend-patterns-reactivity
kind: skill
domain: frontend
category: patterns
generated_at: 2026-06-11T08:14:17.855303+00:00
---

# Reactivity

---
title: Reactivity
summary: Vue 3 reactivity principles — ref, reactive, computed, watch
domain: frontend
category: patterns
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: skill
---

# Reactivity Principles (Vue 3)

## ref و reactive

**ref:** برای primitive values و references به object
✅ **Good:**
```javascript
const count = ref(0);
const user = ref({ name: 'Ali' });
// در template: count، user — unwrap خودکار
```

**reactive:** برای objectها؛ نمی‌توان reassign کرد
✅ **Good:**
```javascript
const state = reactive({ count: 0, name: 'Ali' });
```

## computed

برای derived state که وابسته به reactive data است.
✅ **Good:**
```javascript
const doubled = computed(() => count.value * 2);
const fullName = computed(() => `${firstName.value} ${lastName.value}`);
```

❌ **Bad:** side effect در computed؛ computed باید pure باشد.

## watch و watchEffect

**watch:** برای side effects وقتی یک یا چند منبع تغییر می‌کند
✅ **Good:**
```javascript
watch(count, (newVal, oldVal) => { ... });
watch([a, b], ([newA, newB]) => { ... });
watch(() => obj.id, (id) => { ... }, { immediate: true });
```

**watchEffect:** برای اجرای فوری و track خودکار dependencies
✅ **Good:** وقتی به همه dependencies در یک بلوک نیاز داری

## قوانین

- Reactive statements فقط زمانی اجرا می‌شوند که dependencies تغییر کنند
- از circular dependencies پرهیز کن
- در composables از ref/reactive برگردان و در component استفاده کن
- برای store state از `storeToRefs` استفاده کن تا reactivi
