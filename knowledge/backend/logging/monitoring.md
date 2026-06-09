---
title: Monitoring
summary: Logging & Monitoring — سطوح logging، چه چیزی log شود، Python logging
domain: backend
category: logging
applies_to:
  - "backend/**/*.py"
priority: 50
kind: reference
---

# Logging & Monitoring

## سطوح

* DEBUG: اطلاعات تشخیصی (فقط development)
* INFO: عملیات موفق
* WARNING: اتفاق غیرعادی
* ERROR: خطا با `exc_info=True`
* CRITICAL: خطای جدی

## نمونه

```python
import logging

logger = logging.getLogger(__name__)

logger.info("User %s logged in", user.id)
logger.error("Payment failed for order %s", order.id, exc_info=True)
```

## چه چیزی log کنیم / نکنیم

* ✅ شروع و پایان عملیات مهم
* ✅ خطاها و exceptions
* ✅ تغییرات مهم state
* ❌ passwords، tokens، داده‌های شخصی (PII)
