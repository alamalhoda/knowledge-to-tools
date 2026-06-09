---
title: Settings
summary: Configuration Management — settings، django-environ، environment variables
domain: backend
category: configuration
applies_to:
  - "backend/**/settings*.py"
  - "backend/.env*"
priority: 50
kind: skill
---

# Configuration Management

## الزامات

* settings: `base.py`، `local.py`، `production.py`
* استفاده از `django-environ` یا `os.environ`
* هیچ secret در git commit نشود
* `.env.example` برای نمونه متغیرهای محیطی

## نمونه

```python
# settings/base.py
import os

DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
SECRET_KEY = os.environ["SECRET_KEY"]
```
