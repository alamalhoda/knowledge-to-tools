---
id: frontend-testing-strategy
kind: workflow
domain: frontend
category: testing
generated_at: 2026-06-11T20:40:16.259367+00:00
---

# Strategy

---
title: Strategy
summary: Testing strategy — testing pyramid, coverage targets, Vitest, AAA pattern
domain: frontend
category: testing
applies_to:
  - "frontend/src/**/*.test.js"
  - "frontend/src/**/*.spec.js"
  - "frontend/src/test/**/*"
priority: 50
kind: workflow
---

# Testing Strategy

## Testing Pyramid

```
     /\
    /E2E\         ← 10% (کند، گران)
   /------\
  /  Int.  \      ← 20% (متوسط)
 /----------\
/   Unit     \    ← 70% (سریع، ارزان)
/--------------\
```

## Test Coverage Targets

- ✅ **70%+ overall**
- ✅ **90%+ for utilities/services**
- ✅ **50%+ for components** (focus on logic، not styling)

## Testing Tools (frontend)

- **Unit:** Vitest + Vue Test Utils (@vue/test-utils)
- **E2E:** Playwright (در صورت استفاده)
- **Pinia:** setActivePinia(createPinia()) در setup هر test

## AAA Pattern

**Arrange** (آماده‌سازی): Setup test data، mock dependencies  
**Act** (عمل): Execute function/action  
**Assert** (اثبات): Verify results

## Test Organization

- از test structure منطقی استفاده کن
- از test naming واضح استفاده کن
- از test isolation استفاده کن
- از test fixtures و mocks برای dependencies استفاده کن

