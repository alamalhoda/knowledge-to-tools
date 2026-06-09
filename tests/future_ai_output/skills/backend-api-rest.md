---
id: backend-api-rest
kind: rule
domain: backend
category: api
generated_at: 2026-06-09T20:12:15.471488+00:00
---

# Rest

---
title: Rest
summary: API & REST Rules — HTTP methods، status codes، response structure، versioning، DRF filters
domain: backend
category: api
applies_to:
  - "backend/**/views.py"
  - "backend/**/serializers.py"
  - "backend/**/urls.py"
priority: 50
kind: rule
---

# API & REST Rules (DRF – HARD MODE)

## HTTP Methods

| Method | استفاده |
|--------|---------|
| GET | read (list / retrieve) |
| POST | create |
| PUT | update کامل |
| PATCH | update جزئی |
| DELETE | delete |

## URL Structure

```
✅ /api/v1/vehicles/
✅ /api/v1/vehicles/123/
✅ /api/v1/vehicles/123/services/

❌ /api/getVehicles
❌ /api/createVehicle
```

## Status Codes

* 200 OK
* 201 Created
* 204 No Content
* 400 Bad Request
* 401 Unauthorized
* 403 Forbidden
* 404 Not Found
* 409 Conflict
* 422 Unprocessable Entity (validation)
* 500 Internal Server Error

## Response Structure (یکپارچه)

موفق:

```json
{
  "data": {...},
  "errors": null,
  "meta": {
    "page": 1,
    "total": 100,
    "total_pages": 5
  }
}
```

خطا:

```json
{
  "data": null,
  "errors": ["متن خطا"],
  "meta": {
    "error_code": "VALIDATION_ERROR"
  }
}
```

## Versioning

URL-based: `/api/v1/`

```python
# urls.py
urlpatterns = [
    path("api/v1/", include("khodroban.urls")),
]
```

## Query Params (Filtering/Sorting)

فقط از DRF backends استفاده کن:

* `DjangoFilterBackend` برای filter
* `SearchFilter` برای search
* `OrderingFilter` برای ordering

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_f
