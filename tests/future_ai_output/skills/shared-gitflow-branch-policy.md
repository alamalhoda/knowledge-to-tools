---
id: shared-gitflow-branch-policy
kind: workflow
domain: shared
category: gitflow-branch-policy.mdc
generated_at: 2026-06-10T16:55:23.988209+00:00
---

# Gitflow Branch Policy

---
title: Gitflow Branch Policy
summary: Canonical Git Flow branch policy and guardrails for this project
domain: shared
category: gitflow-branch-policy.mdc
applies_to:
priority: 80
kind: workflow
---

# GitFlow Branch Policy (OilChenger)

## هدف
- این قانون مرجع اصلی Git Flow برای پیشنهادهای AI در این پروژه است.
- AI باید توسعه را فقط روی branchهای کاری انجام دهد و از commit مستقیم روی `main`/`develop` جلوگیری کند.

## مدل شاخه‌ها
- `main`: فقط نسخه پایدار production-ready
- `develop`: شاخه integration (فقط از طریق PR)
- `feature/*`: توسعه قابلیت جدید (از `develop`)
- `bugfix/*`: رفع باگ محیط توسعه (از `develop`)
- `release/*`: آماده‌سازی نسخه (از `develop`)
- `hotfix/*`: رفع فوری production (از `main`)

## قوانین قطعی
1. هرگز commit مستقیم روی `main` یا `develop` پیشنهاد نده.
2. برای شروع کار جدید همیشه اول `develop` را به‌روز کن.
3. branch جدید را صریحاً از شاخه مبدا بساز (`git checkout -b ... develop`).
4. قبل از PR، feature branch را با `origin/develop` همگام کن.
5. اگر rebase انجام شد، فقط `--force-with-lease` مجاز است (نه `--force`).
6. ادغام `feature/*` یا `bugfix/*` به `develop` فقط از طریق Pull Request مجاز است.
7. برای ادغام عادی به `develop` هرگز دستور merge مستقیم محلی (`git merge feature/...`) پیشنهاد نده.

## ترتیب استاندارد شروع Feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/<short-name> develop
```

## نام‌گذاری پیشنهادی
- `feature/add-user-profile`
- `feature/124-login-with-google`
- `bugfix/login-validation`
- `hotfix/
