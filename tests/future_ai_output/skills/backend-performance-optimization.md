---
id: backend-performance-optimization
kind: rule
domain: backend
category: performance
generated_at: 2026-06-11T08:14:17.849923+00:00
---

# Optimization

---
title: Optimization
summary: Performance Rules — N+1، select_related، prefetch_related، caching، cached_property
domain: backend
category: performance
applies_to:
  - "backend/**/views.py"
  - "backend/**/models.py"
priority: 50
kind: rule
---

# Performance Rules (Django)

## N+1 Problem

❌ نادرست:

```python
for order in Order.objects.all():
    print(order.user.email)
```

✅ درست:

```python
for order in Order.objects.select_related("user"):
    print(order.user.email)
```

## Many-to-Many / Reverse FK

```python
orders = Order.objects.prefetch_related("items")
```

## only / defer

```python
users = User.objects.only("id", "email")
```

## Caching

فقط بعد از measurement و profiling:

```python
from django.core.cache import cache

def get_popular_vehicles():
    cached = cache.get("popular_vehicles")
    if cached:
        return cached
    result = list(Vehicle.objects.filter(sales__gte=10)[:10])
    cache.set("popular_vehicles", result, timeout=3600)
    return result
```

## cached_property

```python
from django.utils.functional import cached_property

class Vehicle(models.Model):
    @cached_property
    def total_expense(self):
        return self.expenses.aggregate(Sum("amount"))["amount__sum"] or 0
```

