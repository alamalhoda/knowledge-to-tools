---
title: Rules Audit Checklist
summary: PR-ready checklist for auditing rule changes before merge
domain: shared
category: rules-audit-checklist.mdc
applies_to:
  - ".cursor/rules/**/*.mdc"
  - ".cursor/rules/**/*.md"
priority: 50
kind: workflow
---

# Rules Audit Checklist (PR)

این چک‌لیست قبل از merge تغییرات Ruleها در PR اجرا شود.

## A) Scope and Placement

- [ ] Rule جدید واقعاً عمومی است؟ اگر بله در `share/` قرار گرفته.
- [ ] اگر domain-specific است، در `backend/` یا `frontend/` قرار گرفته.
- [ ] Rule با Rule موجود overlap غیرضروری ندارد.

## B) Frontmatter Validation

- [ ] `description` واضح و کوتاه است.
- [ ] `alwaysApply` فقط وقتی ضروری است `true` شده.
- [ ] برای ruleهای file-specific، `globs` دقیق و کم‌هزینه است.

## C) Conflict and Precedence

- [ ] با `share/rule-precedence.mdc` همخوان است.
- [ ] تعارض با ruleهای موجود بررسی شده و حل شده.
- [ ] اگر rule دیگری جایگزین شده، مسیر جایگزین ذکر شده.

## D) Content Quality

- [ ] Rule actionable است (فقط توضیح نظری نیست).
- [ ] متن تکراری به reference تبدیل شده.
- [ ] مثال‌ها (در صورت وجود) دقیق و به‌روز هستند.
- [ ] دستور ناایمن یا مبهم ندارد.

## E) Documentation Sync

- [ ] `share/README.md` در صورت نیاز به‌روزرسانی شده.
- [ ] `rules/README.md` در صورت تغییر ساختار به‌روزرسانی شده.
- [ ] راهنماهای دامنه (`BACKEND-RULES-GUIDE.md` / `FRONTEND-RULES-GUIDE.md`) در صورت تاثیر آپدیت شده‌اند.

## F) PR Readiness

- [ ] هدف تغییرات Ruleها در PR توضیح داده شده.
- [ ] موارد ریسک/تعارض احتمالی ذکر شده.
- [ ] plan بازگشت (revert) در صورت رفتار نامطلوب مشخص است.
