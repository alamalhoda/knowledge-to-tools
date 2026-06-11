---
id: backend-documentation-file-header
kind: reference
domain: backend
category: documentation
generated_at: 2026-06-11T08:14:17.849103+00:00
---

# File Header

---
title: File Header
summary: File Header & Documentation — Minimal و Full header برای فایل‌های Python
domain: backend
category: documentation
applies_to:
  - "backend/**/*.py"
priority: 50
kind: reference
---

# File Header & Documentation

## Minimal Header (فایل ساده)

```python
"""سرویس سفارش‌ها."""
```

## Full Header (فایل پیچیده)

```python
"""
سرویس ایجاد سفارش (Create Order Service)

فلسفه: منطق ایجاد سفارش در این سرویس متمرکز است. View فقط orchestration می‌کند.

مسئولیت‌ها:
- اعتبارسنجی موجودی کاربر
- ایجاد Order در دیتابیس
- ارسال نوتیفیکیشن

Public API:
- CreateOrderService().execute(user, validated_data) -> Order
"""
```

## استثناها

* `__init__.py` خالی
* فایل‌های config (JSON، YAML)
* فایل‌های بسیار کوچک (<۱۵ خط)

