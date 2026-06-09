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
- `hotfix/security-patch-2026`

## Commit Convention
فرمت:
```text
type(scope): description
```

نوع‌ها:
- `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

نمونه:
```bash
git commit -m "feat(auth): add Google OAuth login flow"
```

## همگام‌سازی Feature قبل از PR (اجباری)
```bash
git checkout feature/<name>
git fetch origin
git merge origin/develop
# یا در صورت نیاز:
# git rebase origin/develop
```

در صورت conflict:
1. فایل‌ها را اصلاح کن
2. `git add <file>`
3. ادامه فرآیند (`git merge --continue` یا `git rebase --continue`)

## Push و PR (اجباری برای ادغام به `develop`)
```bash
git push -u origin feature/<name>
# اگر rebase شده:
git push --force-with-lease origin feature/<name>

# ساخت PR به develop
gh pr create --base develop --head feature/<name> --title "<title>" --body "<body>"
```

PR باید:
- From: `feature/*`
- To: `develop`
- شامل هدف تغییر، خلاصه تغییرات، وضعیت تست/build باشد

## چک‌لیست قبل از PR
- `git status` تمیز یا قابل‌انتظار است
- branch با `origin/develop` به‌روز شده
- conflictها حل شده
- build موفق است
- تست‌های مرتبط پاس شده‌اند
- commit messageها استاندارد هستند

## قاعده ادغام به `develop` (خیلی مهم)
- مسیر مجاز ادغام: `feature/*` یا `bugfix/*` -> Pull Request -> `develop`
- merge مستقیم محلی روی `develop` برای جریان عادی مجاز نیست.
- اگر کاربر درخواست merge مستقیم داد، ابتدا مسیر PR را پیشنهاد بده و دلیل ایمنی را کوتاه توضیح بده.

## رفتار اجباری AI در پیشنهاد دستورات
- قبل از دستورهای حساس، ابتدا `git status` پیشنهاد بده.
- در صورت مشاهده الگوی خطرناک (مثل کار روی `main`/`develop`)، هشدار صریح بده.
- در صورت ابهام در هدف کاربر، اول هدف را شفاف کن و سپس دستور بده.
- برای ادغام به `develop` ابتدا push branch و سپس PR را راهنمایی/اجرا کن.

## پاک‌سازی بعد از PR Merge
```bash
git checkout develop
git pull origin develop
git branch -d feature/<name>
git push origin --delete feature/<name>
```
