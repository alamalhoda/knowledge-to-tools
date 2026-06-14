---
title: Rules Audit Checklist
summary: PR-ready checklist for auditing rule changes before merge
domain: shared
category: rules-audit-checklist.mdc
applies_to:
  - "knowledge/**/*.md"
  - ".kilo/**/*.md"
  - ".opencode/**/*.md"
priority: 50
kind: workflow
---

# Rules Audit Checklist (PR)

این چک‌لیست قبل از merge تغییرات Ruleها در PR اجرا شود.

## A) Scope and Placement

- [ ] Rule جدید واقعاً عمومی است؟ اگر بله در `knowledge/shared/` قرار گرفته.
- [ ] اگر domain-specific است، در `knowledge/backend/` یا `knowledge/frontend/` قرار گرفته.
- [ ] Rule با Rule موجود overlap غیرضروری ندارد.

## B) Frontmatter Validation

- [ ] `description` واضح و کوتاه است.
- [ ] `applies_to` دقیق و کم‌هزینه است.
- [ ] برای ruleهای file-specific، `applies_to` مسیرهای محدود و کم‌هزینه دارد.

## C) Conflict and Precedence

- [ ] با `knowledge/shared/rule-precedence.md` همخوان است.
- [ ] تعارض با ruleهای موجود بررسی شده و حل شده.
- [ ] اگر rule دیگری جایگزین شده، مسیر جایگزین ذکر شده.

## D) Content Quality

- [ ] Rule actionable است (فقط توضیح نظری نیست).
- [ ] متن تکراری به reference تبدیل شده.
- [ ] مثال‌ها (در صورت وجود) دقیق و به‌روز هستند.
- [ ] دستور ناایمن یا مبهم ندارد.

## E) Documentation Sync

- [ ] `knowledge/index.md` در صورت نیاز به‌روزرسانی شده.
- [ ] `knowledge/README.md` در صورت ایجاد ساختار جدید به‌روزرسانی شده.
- [ ] راهنماهای دامنه (`BACKEND-RULES-GUIDE.md` / `FRONTEND-RULES-GUIDE.md`) در صورت تاثیر آپدیت شده‌اند.

## F) PR Readiness

- [ ] هدف تغییرات Ruleها در PR توضیح داده شده.
- [ ] موارد ریسک/تعارض احتمالی ذکر شده.
- [ ] plan بازگشت (revert) در صورت رفتار نامطلوب مشخص است.
