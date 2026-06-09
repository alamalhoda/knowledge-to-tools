---
title: Unit Testing
summary: Unit testing for frontend — Vitest, Vue Test Utils, component and Pinia store tests
domain: frontend
category: testing
applies_to:
  - "frontend/src/**/*.test.js"
  - "frontend/src/**/*.spec.js"
  - "frontend/src/test/**/*"
priority: 50
kind: workflow
---

# Unit Testing (frontend)

## Component Testing

**با Vitest + Vue Test Utils (یا @vue/test-utils):**
- Test user interactions
- Test props و emit
- Test accessibility (در صورت استفاده از Testing Library)

**الگو:**
- Mount component با `mount()` و options (props، global.plugins برای Pinia/Router)
- Query elements (by role، label، text)
- Fire events (`wrapper.find('button').trigger('click')`)
- Assert expectations (`expect(wrapper.text()).toContain(...)`)

## Pinia Store Testing

**الگو:**
- ایجاد store با `setActivePinia(createPinia())` قبل از هر test
- Test initial state
- Test actions و mutations روی state
- Test getters (computed)
- Test error handling

## Utility و Service Testing

- Pure functions
- Edge cases (null، empty، invalid)
- Error handling
- Mock axios/fetch برای service tests

## Best Practices

- Test behavior، not implementation
- Test user interactions از دید کاربر
- Isolate tests (no shared state بین tests)
- Clear test names: `test('submits form when button clicked', ...)`
- AAA pattern: Arrange، Act، Assert
