---
title: Strategy
summary: Testing Rules — Test pyramid، AAA pattern، APITestCase، coverage، naming
domain: backend
category: testing
applies_to:
  - "backend/**/test*.py"
  - "backend/**/tests/**/*.py"
priority: 50
kind: workflow
---

# Testing Rules

## Test Pyramid

* Unit: ۷۰٪
* Integration: ۲۰٪
* E2E: ۱۰٪

## AAA Pattern

```python
def test_create_order():
    # Arrange
    user = UserFactory()
    data = {"total": 1000}

    # Act
    response = client.post("/api/v1/orders/", data, user=user)

    # Assert
    assert response.status_code == 201
```

## Django APITestCase

❌ نادرست:

```python
# no tests
```

✅ درست:

```python
from rest_framework.test import APITestCase

class OrderAPITest(APITestCase):
    def test_unauthorized_returns_401(self):
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 401)

    def test_authenticated_can_list_own_orders(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/orders/")
        self.assertEqual(response.status_code, 200)
```

## Naming

`test_<action>_<scenario>_<expected>`

## Coverage

هدف ≥ ۸۰٪ برای مسیرهای حیاتی:

```bash
pytest --cov=khodroban --cov-report=html
```
