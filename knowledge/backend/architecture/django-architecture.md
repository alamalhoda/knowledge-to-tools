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
```

## Serializer Is the Contract

❌ نادرست:

```python
# validation در view
if "email" not in request.data:
    raise ValidationError("Email required")
```

✅ درست:

```python
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["id", "email", "name"]
```

## No Fat Serializers

❌ نادرست:

```python
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        charge_user()
        send_notification()
        return Order.objects.create(**validated_data)
```

✅ درست:

```python
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CreateOrderService().execute(
            user=self.context["request"].user,
            validated_data=validated_data,
        )
```
