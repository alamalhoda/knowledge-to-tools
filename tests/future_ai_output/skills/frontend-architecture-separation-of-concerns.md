---
id: frontend-architecture-separation-of-concerns
kind: architecture
domain: frontend
category: architecture
generated_at: 2026-06-09T20:12:15.481907+00:00
---

# Separation Of Concerns

---
title: Separation Of Concerns
summary: Separation of concerns principles for separating UI logic, business logic, and data access
domain: frontend
category: architecture
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: architecture
---

# Separation of Concerns

جداسازی منطق UI، منطق تجاری (business logic)، و دسترسی به داده.

## Layer Separation

### Presentational Components
- فقط UI rendering
- بدون business logic
- بدون direct API calls
- فقط props می‌گیرد و emit می‌کند

### Container Components (Views)
- مدیریت state و logic
- Data fetching coordination
- Event handling

### Services
- API calls
- Data transformation
- Business logic (pure functions)

### Stores (Pinia)
- Global state management
- Reactive state updates
- State persistence (در صورت نیاز)

## Anti-Pattern

❌ **Bad:** همه چیز در یک کامپوننت
- API calls در component
- Business logic در component
- UI rendering در همان component

✅ **Good:** جداسازی کامل
- Service برای API
- Pinia store برای state
- Component فقط UI

