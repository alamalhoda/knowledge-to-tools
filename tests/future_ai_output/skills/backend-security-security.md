---
id: backend-security-security
kind: rule
domain: backend
category: security
generated_at: 2026-06-11T08:14:17.850298+00:00
---

# Security

---
title: Security
summary: Security Rules — validation، permissions، throttling، secrets، password hashing
domain: backend
category: security
applies_to:
  - "backend/**/views.py"
  - "backend/**/serializers.py"
  - "backend/**/settings*.py"
priority: 50
kind: rule
---

# Security Rules

## الزامات

* validation فقط در Serializer
* جلوگیری از SQL injection با ORM (هیچ raw SQL با string concatenation)
* secrets فقط در environment variables
* پیام خطای production generic (بدون stack trace)
* `permissions` + `throttling` الزامی برای ViewSetها

## Permissions

❌ نادرست:

```python
class OrderViewSet(ModelViewSet):
    pass
```

✅ درست:

```python
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottle]
```

## Secrets

```python
# settings.py
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}
```

## Password Hashing

همیشه از `django.contrib.auth.hashers` استفاده کن:

```python
from django.contrib.auth.hashers import make_password, check_password

hashed = make_password(plain_password)
check_password(plain_password, hashed)
```

