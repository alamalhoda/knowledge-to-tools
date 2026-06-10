---
id: backend-patterns-progressive-development
kind: workflow
domain: backend
category: patterns
generated_at: 2026-06-10T16:55:23.956195+00:00
---

# Progressive Development

---
title: Progressive Development
summary: Progressive Development — Feature flags، backward compatibility، deprecation
domain: backend
category: patterns
applies_to:
  - "backend/**/*.py"
priority: 50
kind: workflow
---

# Progressive Development

## Feature Flags

```python
# settings.py
FEATURE_FLAGS = {
    "new_payment": os.environ.get("ENABLE_NEW_PAYMENT", "false") == "true",
}

# usage
if settings.FEATURE_FLAGS["new_payment"]:
    return new_payment_service.process(order)
return legacy_payment_service.process(order)
```

## Backward Compatibility

* API قدیمی را فوراً حذف نکن
* deprecation notice قبل از حذف

```python
import warnings

def old_endpoint(request):
    warnings.warn("Use /api/v2/... instead", DeprecationWarning, stacklevel=2)
    return new_endpoint(request)
```

