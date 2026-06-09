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
```

✅ درست / Correct:

```python
class CreateOrderService:
    def execute(self, user, validated_data):
        return Order.objects.create(**validated_data, user=user)


class CancelOrderService:
    def execute(self, order):
        if order.status != OrderStatus.PENDING:
            raise DomainError("Cannot cancel")
        order.status = OrderStatus.CANCELLED
        order.save()
        return order


class OrderNotificationService:
    def send_created(self, order): ...
    def send_cancelled(self, order): ...
```

---

## Single Source of Truth (SSOT) — منبع یگانه حقیقت

**توضیح:** هر منطق (مثل validation، محاسبه مالیات) باید در یک جا تعریف شود. تکرار در چند فایل نقض SSOT است.

**Explanation:** Each logic (e.g., validation, tax calculation) must be defined in one place. Duplicating across files violates SSOT.

❌ نادرست / Wrong:

```python
# در views.py
def create_order(request):
    if request.user.profile.balance < 0:
        raise ValidationError("No balance")

# در serializers.py — همان منطق تکرار شده!
class OrderSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if self.context["request"].user.profile.balance < 0:
            raise ValidationError("No balance")
```

✅ درست / Correct:

```python
# فقط در service — یک منبع حقیقت
class CreateOrderService:
    def execute(self, user, validated_data):
        if user.profile.balance < 0:
            raise DomainError("موجودی کافی نیست / Insufficient balance")
        return Order.objects.create(**validated_data, user=user)


# در serializer — فقط فراخوانی service
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CreateOrderService().execute(
            user=self.context["request"].user,
            validated_data=validated_data,
        )
```

---

## DRY — تکرار نکن

**توضیح:** اگر منطق در دو جا تکرار شد، آن را به تابع یا کلاس واحد استخراج کن.

**Explanation:** If logic is duplicated in two places, extract it into a single function or class.

❌ نادرست / Wrong:

```python
# در چند جا تکرار شده
def register_user(email, password):
    if len(password) < 8:
        raise ValidationError("Password too short")

def change_password(user, new_password):
    if len(new_password) < 8:
        raise ValidationError("Password too short")
```

✅ درست / Correct:

```python
MIN_PASSWORD_LENGTH = 8


def validate_password(password: str) -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError("رمز عبور حداقل ۸ کاراکتر باشد")


def register_user(email: str, password: str):
    validate_password(password)
    # ...


def change_password(user, new_password: str):
    validate_password(new_password)
    # ...
```

---

## Separation of Concerns (SoC) — جداسازی دغدغه‌ها

**توضیح:** View فقط orchestration؛ Service برای business logic؛ Serializer فقط validation و serialization.

**Explanation:** View only orchestrates; Service holds business logic; Serializer only validates and serializes.

❌ نادرست / Wrong:

```python
# business logic در View
class OrderViewSet(ModelViewSet):
    def create(self, request):
        if request.user.profile.balance < 0:
            raise ValidationError("No balance")
        order = Order.objects.create(
            user=request.user,
            total=request.data["total"],
        )
        send_email(order.user.email, "Order created")
        return Response(OrderSerializer(order).data)
```

✅ درست / Correct:

```python
# View فقط orchestration
class OrderViewSet(ModelViewSet):
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = CreateOrderService().execute(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return Response(OrderSerializer(order).data, status=201)


# Service — business logic
class CreateOrderService:
    def execute(self, user, validated_data):
        if user.profile.balance < 0:
            raise DomainError("Insufficient balance")
        order = Order.objects.create(user=user, **validated_data)
        OrderNotificationService().send_created(order)
        return order
```
