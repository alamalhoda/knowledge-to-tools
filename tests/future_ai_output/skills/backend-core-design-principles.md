---
id: backend-core-design-principles
kind: principle
domain: backend
category: core
generated_at: 2026-06-11T08:14:17.848283+00:00
---

# Design Principles

---
title: Design Principles
summary: Backend design principles and examples aligned with shared engineering principles
domain: backend
category: core
applies_to:
  - "backend/**/*.py"
priority: 50
kind: principle
---

# Design Principles (اصول طراحی)

راهنمای طراحی backend Django با مثال‌های عملی.

**English:** Backend-focused design guidance for Django with practical examples.

---

## Shared Source of Truth

- اصول عمومی (SSOT/SoC/DRY/KISS/YAGNI/Explicitness) در
  `.cursor/rules/share/engineering-principles.mdc` تعریف شده‌اند.
- اگر اختلافی وجود داشت، rule تخصصی backend در این فایل اولویت دارد.

---

## God Class (کلاس خدا) — نقض SRP

**توضیح:** کلاسی که چندین مسئولیت دارد و باید به کلاس‌های کوچک‌تر تقسیم شود.

**Explanation:** A class with multiple responsibilities that should be split into smaller, focused classes.

❌ نادرست / Wrong:

```python
class OrderManager:
    """همه کارها در یک کلاس — نقض SRP"""

    def create(self, user, data):
        self._validate(data)
        order = Order.objects.create(**data, user=user)
        self._send_notification(order)
        return order

    def cancel(self, order):
        if order.status != "PENDING":
            raise ValidationError("Cannot cancel")
        order.status = "CANCELLED"
        order.save()
        self._send_refund(order)

    def refund(self, order):
        # منطق refund...
        pass

    def _validate(self, data): ...
    def _send_notification(self, order): ...
    def _send_refund(self, order): ...
`
