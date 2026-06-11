---
id: shared-rule-authoring-standard
kind: rule
domain: shared
category: rule-authoring-standard.mdc
generated_at: 2026-06-11T08:14:17.862161+00:00
---

# Rule Authoring Standard

---
title: Rule Authoring Standard
summary: Authoring standards for creating and maintaining Cursor rule files
domain: shared
category: rule-authoring-standard.mdc
applies_to:
  - ".cursor/rules/**/*.mdc"
  - ".cursor/rules/**/*.md"
priority: 50
kind: rule
---

# Rule Authoring Standard

استاندارد نگارش Ruleها برای یکدستی، نگهداری ساده، و کاهش تداخل.

## Structure

- هر Rule باید frontmatter معتبر داشته باشد:
  - `description`
  - `alwaysApply` یا `globs` (بر اساس نیاز)
- عنوان واضح و محتوای action-oriented داشته باشد.
- یک Rule = یک concern اصلی (از ruleهای God پرهیز کن).

## Placement Policy

- قوانین **عمومی/جهان‌شمول** → `share/`
- قوانین **تخصصی frontend** → `frontend/`
- قوانین **تخصصی backend** → `backend/`
- قوانین deprecated:
  - `alwaysApply: false`
  - در توضیح، `replaced by <path>` ذکر شود

## AlwaysApply Budget

- هدف پروژه: حداکثر **۵ Rule** با `alwaysApply: true`
- `alwaysApply: true` فقط برای قواعد global و کم‌حجم در `share/`
- Ruleهای domain-specific باید `alwaysApply: false` باشند و با `globs` دقیق فعال شوند
- اگر Rule جدید نیاز به `alwaysApply: true` داشت:
  1. دلیل صریح بنویس
  2. اثر آن بر context window را بررسی کن
  3. در صورت امکان یک Rule قدیمی را به حالت scoped تبدیل کن

## Naming Convention

- نام فایل‌ها: `kebab-case.mdc`
- الگوی پیشنهادی:
  - `<topic>-policy.mdc`
  - `<topic>-checklist.mdc`
  - `<topic>-standards.mdc`

## Content Quality

- قوانین کوتاه، شفاف، و قابل اجرا باشند.
- از مثال‌های `Bad/Good` فقط وقتی کمک می‌کند استفاده کن.
- تکرار محتو
