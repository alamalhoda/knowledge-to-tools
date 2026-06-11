---
id: shared-gitguardian-secrets-policy
kind: policy
domain: shared
category: gitguardian-secrets-policy.mdc
generated_at: 2026-06-11T08:14:17.861499+00:00
---

# Gitguardian Secrets Policy

---
title: Gitguardian Secrets Policy
summary: Prevent GitGuardian secret detections from hardcoded credential-like strings
domain: shared
category: gitguardian-secrets-policy.mdc
applies_to:
  - "backend/**/*.py"
  - "frontend/src/**/*.{js,ts,vue}"
  - "shared/**/*.{js,ts}"
priority: 50
kind: policy
---

# GitGuardian Secrets Policy

## Goal

جلوگیری از hard-code شدن رشته‌هایی که شبیه credential هستند (password/token/api key) و باعث fail شدن GitGuardian می‌شوند.

## Required Rules

- هیچ credential-like literal (برای password/token/api-key/secret) در کد یا تست ثبت نکن.
- در تست‌ها مقدار credential را فقط در runtime تولید کن و همان مقدار را در create/login reuse کن.
- برای Django تست‌ها از تولید تصادفی مثل `get_random_string(...)` استفاده کن.
- هر payload احراز هویت باید credential را از متغیر runtime بگیرد، نه از string ثابت.
- secrets واقعی فقط از env/config امن خوانده شوند؛ هرگز در repo ذخیره نشوند.

## Example

✅ Good:
```python
from django.utils.crypto import get_random_string

test_password = get_random_string(12)
User.objects.create_user(username="u1", password=test_password)
```

