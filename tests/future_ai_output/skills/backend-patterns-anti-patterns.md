---
id: backend-patterns-anti-patterns
kind: reference
domain: backend
category: patterns
generated_at: 2026-06-11T20:40:16.249091+00:00
---

# Anti Patterns

---
title: Anti Patterns
summary: Anti-Patterns — God class، magic numbers، fat serializers، business logic in views
domain: backend
category: patterns
applies_to:
  - "backend/**/*.py"
priority: 50
kind: reference
---

# Anti-Patterns

قاعده‌های عمومی anti-pattern در
`.cursor/rules/share/code-quality-baseline.mdc`
تعریف شده‌اند. موارد این فایل مکمل backend هستند.

* **God class** — کلاسی که همه کارها را انجام می‌دهد
* **Magic numbers** — از constants استفاده کن
* **Circular dependencies** — وابستگی دایره‌ای ممنوع
* **Fat serializers** — منطق تجاری در Serializer نگذار
* **Business logic in views** — View فقط orchestration
* **Hard-coded secrets** — secrets فقط در env
* **Raw SQL با string concatenation** — همیشه از ORM
* **Premature optimization** — فقط بعد از measurement

