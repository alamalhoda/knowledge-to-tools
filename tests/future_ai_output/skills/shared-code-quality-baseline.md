---
id: shared-code-quality-baseline
kind: rule
domain: shared
category: code-quality-baseline.mdc
generated_at: 2026-06-11T20:40:16.261954+00:00
---

# Code Quality Baseline

---
title: Code Quality Baseline
summary: Universal code quality baseline for all code changes
domain: shared
category: code-quality-baseline.mdc
applies_to:
priority: 80
kind: rule
---

# Code Quality Baseline (Shared)

این baseline در کل پروژه اعمال می‌شود و قوانین تخصصی هر دامنه آن را تکمیل می‌کنند.

## Baseline Rules

- کد باید خوانا، قابل فهم و قابل نگهداری باشد.
- از نام‌های توصیفی برای فایل‌ها، متغیرها، توابع، و کلاس‌ها استفاده کن.
- از `magic numbers` و `magic strings` پرهیز کن؛ از constant یا config استفاده کن.
- از کامنت غیرضروری پرهیز کن؛ فقط منطق پیچیده را توضیح بده.
- side effect پنهان ایجاد نکن؛ رفتار مهم باید قابل پیش‌بینی باشد.
- secrets (token/password/api-key) نباید hard-code شوند؛ فقط env/config امن.
- برای تغییرات بحرانی یا رفتارهای حیاتی، تست یا plan تست ارائه بده.

## Scope Note

- قوانین naming/framework-specific را ruleهای همان دامنه تعیین می‌کنند.

