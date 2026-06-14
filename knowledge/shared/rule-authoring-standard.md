---
title: Rule Authoring Standard
summary: Authoring standards for creating and maintaining Cursor rule files
domain: shared
category: rule-authoring-standard.mdc
applies_to:
  - "knowledge/**/*.md"
  - ".kilo/**/*.md"
  - ".opencode/**/*.md"
priority: 50
kind: rule
---

# Rule Authoring Standard

استاندارد نگارش Ruleها برای یکدستی، نگهداری ساده، و کاهش تداخل.

## Structure

- هر Rule باید metadata معتبر داشته باشد:
  - `description`
  - `applies_to` برای فعال‌سازی بر اساس مسیر
- عنوان واضح و محتوای action-oriented داشته باشد.
- یک Rule = یک concern اصلی (از ruleهای God پرهیز کن).

## Placement Policy

- قوانین **عمومی/جهان‌شمول** → `knowledge/shared/`
- قوانین **تخصصی frontend** → `knowledge/frontend/`
- قوانین **تخصصی backend** → `knowledge/backend/`
- قوانین deprecated:
  - `status: deprecated`
  - در توضیح، `replaced by <path>` ذکر شود

## AlwaysApply Budget

- هدف پروژه: حداکثر **۵ Rule** با `priority` بالا و scope گسترده
- `priority` بالا فقط برای قواعد global و کم‌حجم در `knowledge/shared/`
- Ruleهای domain-specific باید با `applies_to` دقیق فعال شوند
- اگر Rule جدید نیاز به scope گسترده داشت:
  1. دلیل صریح بنویس
  2. اثر آن بر context window را بررسی کن
  3. در صورت امکان یک Rule قدیمی را به حالت scoped تبدیل کن

## Naming Convention

- نام فایل‌ها: `kebab-case.md`
- الگوی پیشنهادی:
  - `<topic>-policy.md`
  - `<topic>-checklist.md`
  - `<topic>-standards.md`

## Content Quality

- قوانین کوتاه، شفاف، و قابل اجرا باشند.
- از مثال‌های `Bad/Good` فقط وقتی کمک می‌کند استفاده کن.
- تکرار محتوای موجود را به ارجاع تبدیل کن، نه کپی.
- دستورات پرخطر باید صریحاً با guardrail همراه باشند.
