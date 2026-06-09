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

ViewSetها باید `permission_classes` و در صورت نیاز `throttle_classes` داشته باشند.

**English:** ViewSets must have `permission_classes` and optionally `throttle_classes`.

❌ نادرست / Wrong:

```python
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # بدون permission!
```

✅ درست / Correct:

```python
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottle]
```

---

## 2. Serializer فقط validation؟ / Serializer for validation only?

منطق تجاری در Serializer نگذار؛ فقط validation و فراخوانی service.

**English:** Don't put business logic in Serializer; only validation and service call.

❌ نادرست / Wrong:

```python
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        charge_payment(validated_data["amount"])
        order = Order.objects.create(**validated_data)
        send_notification(order)
        return order
```

✅ درست / Correct:

```python
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CreateOrderService().execute(
            user=self.context["request"].user,
            validated_data=validated_data,
        )
```

---

## 3. Business logic در service؟ / Business logic in service?

منطق تجاری در Service؛ View فقط orchestration.

**English:** Business logic in Service; View only orchestrates.

❌ نادرست / Wrong:

```python
class OrderViewSet(ModelViewSet):
    def create(self, request):
        if request.user.profile.balance < 0:
            raise ValidationError("No balance")
        order = Order.objects.create(user=request.user, **request.data)
        return Response(OrderSerializer(order).data)
```

✅ درست / Correct:

```python
class OrderViewSet(ModelViewSet):
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = CreateOrderService().execute(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return Response(OrderSerializer(order).data, status=201)
```

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

برای foreign key: `select_related`. برای many-to-many / reverse FK: `prefetch_related`.

**English:** For FK: `select_related`. For M2M / reverse FK: `prefetch_related`.

❌ نادرست / Wrong:

```python
for order in Order.objects.all():
    print(order.user.email)  # هر بار query جدید — N+1!
```

✅ درست / Correct:

```python
for order in Order.objects.select_related("user"):
    print(order.user.email)  # یک query

# برای many-to-many یا reverse FK
orders = Order.objects.prefetch_related("items")
```

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
