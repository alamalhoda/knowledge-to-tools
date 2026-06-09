---
title: Pinia
summary: Pinia store patterns — defineStore, state, getters, actions — and usage in Vue components
domain: frontend
category: state
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/stores/**/*.js"
priority: 50
kind: skill
---

# State Management (Pinia)

## defineStore

از Composition API style (setup function) یا Options style استفاده کن. برای frontend ترجیحاً setup style با ref/reactive.

✅ **Good (Setup store):**
```javascript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const isLoggedIn = computed(() => !!user.value);

  function setUser(u) { user.value = u; }
  function logout() { user.value = null; }

  return { user, isLoggedIn, setUser, logout };
});
```

## State و Getters و Actions

- **State:** داده‌های reactive (ref/reactive در setup store)
- **Getters:** از computed برای derived state استفاده کن
- **Actions:** توابع async یا sync برای تغییر state و side effects (API calls در action یا در service و سپس فراخوانی از action)

## استفاده در کامپوننت

✅ **Good:** برای حفظ reactivity از storeToRefs استفاده کن
```vue
<script setup>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const { user, isLoggedIn } = storeToRefs(authStore);
const { logout } = authStore;
</script>
```

❌ **Bad:** destructuring مستقیم از store بدون storeToRefs — reactivity از بین می‌رود.

## قوانین

- یک store یک حوزه مسئولیت (مثلاً auth، vehicle، ui)
- از نام‌گذاری camelCase برای فایل store استفاده کن: `auth.js`, `vehicle.js`
- API calls را در service انجام بده و در action فقط store را به‌روز کن؛ یا در action از service استفاده کن
- از persist plugin فقط در صورت نیاز (مثلاً auth token)
