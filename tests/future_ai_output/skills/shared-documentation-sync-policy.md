---
id: shared-documentation-sync-policy
kind: policy
domain: shared
category: documentation-sync-policy.mdc
generated_at: 2026-06-11T08:14:17.860434+00:00
---

# Documentation Sync Policy

---
title: Documentation Sync Policy
summary: Keep TODO/README/PLAN and project docs synchronized after major changes and before every PR
domain: shared
category: documentation-sync-policy.mdc
applies_to:
  - "backend/**/*.py"
  - "frontend/src/**/*.{js,ts,vue}"
  - "shared/**/*.{js,ts}"
  - "docs/**/*.md"
  - "**/*README*.md"
  - "**/*TODO*.md"
  - "**/*PLAN*.md"
priority: 50
kind: policy
---

# Documentation Sync Policy

## Goal

بعد از تغییرات مهم (به‌خصوص قبل از ساخت PR)، مستندات پروژه باید با وضعیت واقعی کد همگام شوند.

## Mandatory Checklist (Before PR)

1. اثر تغییر را تعیین کن: frontend / backend / shared / API / process.
2. فایل‌های مستنداتی مرتبط را بازبینی و در صورت نیاز به‌روز کن.
3. اگر تغییری لازم نبود، دلیل "عدم نیاز به تغییر مستندات" را در توضیح PR ذکر کن.

## Minimum Docs Coverage

- تغییرات cross-domain یا اولویت‌ها -> `TODO.md`
- تغییرات backend -> `backend/TODO.md`, `backend/README.md`
- تغییرات frontend -> `frontend/TODO.md`, `frontend/README.md`
- تغییرات roadmap/phase -> `frontend/IMPLEMENTATION_PLAN.md`
- تغییرات قرارداد API -> `docs/development/API_CONTRACT_REGISTRY.md`
- تغییرات وضعیت flow صفحات -> `docs/development/PAGE_REVIEW_LOG.md`

## PR Rule

- هر PR باید یکی از این دو حالت را شفاف داشته باشد:
  - `Docs updated` (فایل‌های به‌روز شده ذکر شوند)
  - `Docs impact: none` (به‌همراه دلیل روشن)

## Guardrails

- وضعیت انجام کار را حدسی یا optimistic ثبت نکن؛ فقط بر اساس شواهد کد/تست.
- اگر تغییر behavior یا contract رخ داده، به‌روزرسانی doc را به PR بع
