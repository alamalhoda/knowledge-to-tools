---
id: backend-architecture-django-architecture
kind: architecture
domain: backend
category: architecture
generated_at: 2026-06-11T08:14:17.847384+00:00
---

# Django Architecture

---
title: Django Architecture
summary: Django Architecture — App-based structure، View/Service/Serializer، business logic placement
domain: backend
category: architecture
applies_to:
  - "backend/**/views.py"
  - "backend/**/serializers.py"
  - "backend/**/urls.py"
priority: 50
kind: architecture
---

# Django Architecture Rules

## ساختار App-based

```
khodroban_prj/          # پروژه Django
├── khodroban_prj/      # تنظیمات پروژه
│   ├── settings.py
│   └── urls.py
├── khodroban/          # اپ اصلی
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
└── manage.py
```

## Business Logic Placement

* View فقط orchestration
* Service برای business logic
* Serializer فقط validation و serialization
* Circular dependency ممنوع

❌ نادرست (در View):

```python
class OrderViewSet(ModelViewSet):
    def create(self, request):
        if request.user.profile.balance < 0:
            raise ValidationError("No balance")
```

✅ درست (Service):

```python
class CreateOrderService:
    def execute(self, user, validated_data):
        if user.profile.balance < 0:
            raise DomainError("No balance")
        return Order.objects.create(**validated_data, user=user)
```

## ViewSet Only

❌ نادرست:

```python
class CreateOrder(APIView):
    def post(self, request): ...
```

✅ درست:

```python
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

