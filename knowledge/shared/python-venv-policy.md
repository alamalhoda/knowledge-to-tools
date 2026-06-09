---
title: Python Venv Policy
summary: Before running Python commands in this project, the virtual environment must be activated
domain: shared
category: python-venv-policy.mdc
applies_to:
priority: 80
kind: policy
---

# Python Virtual Environment (Project Policy)

قبل از اجرای هر دستور پایتون در این پروژه، محیط مجازی باید فعال شود.

## قانون اجباری

- **هرگز** دستور `python`، `python3`، `pip`، `manage.py`، `pytest` و مانند آن را **بدون فعال‌سازی محیط مجازی** پیشنهاد یا اجرا نکن.
- محیط مجازی پروژه: `backend/.venv`
- فعال‌سازی از ریشه پروژه:
  ```bash
  source backend/.venv/bin/activate
  ```
- پس از فعال‌سازی، دستورات پایتون را در همان شل اجرا کن (مثلاً `python manage.py test ...`).

## ترتیب پیشنهادی

1. در صورت نیاز به اجرای دستور پایتون، اول محیط مجازی را فعال کن.
2. سپس دستور موردنظر را در همان session اجرا کن.

## Scope

- این قانون برای همه دستورات مرتبط با backend Django و اسکریپت‌های پایتون در این مونورپو اعمال می‌شود.
