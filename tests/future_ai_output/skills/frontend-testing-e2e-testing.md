---
id: frontend-testing-e2e-testing
kind: workflow
domain: frontend
category: testing
generated_at: 2026-06-10T16:55:23.978778+00:00
---

# E2E Testing

---
title: E2E Testing
summary: End-to-end testing guidelines for critical user flows and visual regression
domain: frontend
category: testing
applies_to:
  - "frontend/**/*.e2e.js"
  - "frontend/e2e/**/*"
priority: 50
kind: workflow
---

# E2E Testing

## Test Coverage

**Test critical user flows:**
- Authentication (login / signup)
- Form submissions
- Navigation
- Main features (e.g. vehicle list، reminders)

## Test Structure

**با Playwright (در صورت استفاده):**
- Navigate to page
- Interact with elements
- Assert expectations
- Verify URLs

## Best Practices

- Test real user scenarios
- Use data-testid برای stable selectors
- Wait for network idle
- Cleanup بعد از tests
- Screenshots برای debugging

## Visual Regression

- Baseline screenshots
- Compare on CI/CD
- Update baselines هنگام intentional changes

