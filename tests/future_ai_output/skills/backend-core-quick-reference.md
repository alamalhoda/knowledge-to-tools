---
id: backend-core-quick-reference
kind: reference
domain: backend
category: core
generated_at: 2026-06-10T16:55:23.952577+00:00
---

# Quick Reference

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

✅ درست / 
