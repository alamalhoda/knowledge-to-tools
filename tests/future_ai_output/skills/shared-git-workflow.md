---
id: shared-git-workflow
kind: workflow
domain: shared
category: git-workflow.mdc
generated_at: 2026-06-11T08:14:17.861077+00:00
---

# Git Workflow

---
title: Git Workflow
summary: Backend git workflow notes aligned with share/gitflow-unified
domain: shared
category: git-workflow.mdc
applies_to:
  - "backend/**/*"
  - ".github/**/*"
priority: 50
kind: workflow
---

# Git & Version Control

## Source of Truth

- مرجع اصلی و الزامی Git Flow در پروژه:
  - `.cursor/rules/share/gitflow-branch-policy.mdc`
- اگر هر اختلافی وجود داشت، همیشه `gitflow-branch-policy.mdc` اولویت دارد.

## Branch Strategy (Aligned)

* `main`: production
* `develop`: integration
* `feature/*`: feature جدید
* `bugfix/*`: رفع باگ محیط توسعه
* `release/*`: آماده‌سازی release
* `hotfix/*`: رفع فوری production

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-payment develop
```

## Commit Convention

```
type(scope): description

# انواع:
feat:   feature جدید
fix:    رفع باگ
refactor: تغییر بدون تغییر رفتار
test:   تست
docs:   مستندات
chore:  نگهداری
```

مثال:

```
feat(auth): add JWT authentication to user login
```

## High-Risk Change (تغییر پرخطر)

AI باید این موارد را **explicitly اعلام خطر** کند:

* تغییر در database schema
* تغییر در API contract (breaking changes)
* تغییر در authentication/authorization
* refactoring بیش از ۱۰۰ خط
* افزودن dependency جدید
* حذف field یا endpoint

