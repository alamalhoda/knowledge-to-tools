---
title: Quick Reference
summary: Quick Reference — AI Checklist برای backend Django
domain: backend
category: core
applies_to:
  - "backend/**/*.py"
priority: 50
kind: reference
---

# Quick Reference (AI Checklist)

چک‌لیست سریع قبل از ارائه کد. هر مورد را بررسی کن.

**English:** Quick checklist before submitting code. Verify each item.

---

## 1. Permission دارد؟ / Permissions defined?

ViewSetها باید `permission_classes` و در صورت نیاز `throttle_classes` داشته باشند. جزئیات و مثال در
`knowledge/backend/security/security.md`.

---

## 2. Serializer فقط validation؟ / Serializer for validation only?

منطق تجاری در Serializer نگذار؛ فقط validation و فراخوانی service. جزئیات و مثال در
`knowledge/backend/architecture/django-architecture.md`.

---

## 3. Business logic در service؟ / Business logic in service?

منطق تجاری در Service؛ View فقط orchestration. جزئیات و مثال در
`knowledge/backend/architecture/django-architecture.md`.

---

## 4. Migration امن است؟ / Migration safe?

همیشه migration بساز؛ دیتابیس را دستی تغییر نده. فیلدهای جدید با default یا nullable.

**English:** Always create migrations; don't change DB manually. New fields with default or nullable.

❌ نادرست / Wrong:

```python
# افزودن فیلد بدون default — migration شکست می‌خورد روی رکوردهای موجود
class Order(models.Model):
    status = models.CharField(max_length=20)  # بدون default
```

✅ درست / Correct:

```python
class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "در انتظار"

class Order(models.Model):
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
```

---

## 5. Test اضافه شده؟ / Tests added?

API و منطق حیاتی باید تست داشته باشند.

**English:** API and critical logic must have tests.

❌ نادرست / Wrong:

```python
# هیچ test برای endpoint جدید
# No tests for new endpoint
```

✅ درست / Correct:

```python
class OrderAPITest(APITestCase):
    def test_unauthorized_returns_401(self):
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_can_list_own_orders(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 200)
```

---

## 6. N+1 برطرف شده؟ / N+1 fixed?

برای foreign key: `select_related`. برای many-to-many / reverse FK: `prefetch_related`. جزئیات و مثال در
`knowledge/backend/performance/optimization.md`.

---

## 7. Secrets در env؟ / Secrets in env?

رمزها، API keys و tokens در کد نگذار؛ از environment variables استفاده کن.

**English:** Don't put passwords, API keys, tokens in code; use environment variables.

❌ نادرست / Wrong:

```python
SECRET_KEY = "my-hardcoded-secret"
DB_PASSWORD = "admin123"
```

✅ درست / Correct:

```python
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```

---

## 8. Type hints برای توابع عمومی؟ / Type hints for public functions?

توابع عمومی باید type hints داشته باشند.

**English:** Public functions must have type hints.

❌ نادرست / Wrong:

```python
def process_order(order):
    return order.total * 1.09
```

✅ درست / Correct:

```python
def process_order(order: Order) -> Decimal:
    return order.total * Decimal("1.09")
```
