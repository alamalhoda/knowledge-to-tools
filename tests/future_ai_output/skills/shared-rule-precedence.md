---
id: shared-rule-precedence
kind: rule
domain: shared
category: rule-precedence.mdc
generated_at: 2026-06-11T20:40:16.264611+00:00
---

# Rule Precedence

---
title: Rule Precedence
summary: Rule precedence and conflict resolution policy for all Cursor rules
domain: shared
category: rule-precedence.mdc
applies_to:
priority: 80
kind: rule
---

# Rule Precedence

این فایل ترتیب اولویت Ruleها را مشخص می‌کند تا تضادها قابل حل باشند.

## Precedence Order

1. **System/Platform constraints**
2. **Repository global rules** (`share/*`)
3. **Domain rules** (`backend/*` یا `frontend/*`) بر اساس مسیر فایل
4. **File-specific rules** (glob محدودتر) نسبت به glob کلی‌تر
5. **Style preferences** (کم‌اولویت‌تر از correctness/security)

## Conflict Resolution

- در تعارض بین `share` و domain، اگر موضوع domain-specific است، rule دامنه ارجح است.
- در تعارض بین دو rule هم‌سطح:
  - rule با scope محدودتر ارجح است.
  - اگر scope برابر بود، rule جدیدتر/شفاف‌تر را مبنا بگیر.
- در تعارض امنیت/درستی با style/performance، اولویت با **security/correctness** است.

## Mandatory Behavior

- اگر conflict قابل حل نبود، AI باید:
  1. تعارض را صریح اعلام کند
  2. ریسک هر گزینه را کوتاه بگوید
  3. سؤال روشن برای تصمیم نهایی بپرسد

## Scope Mapping

- فایل‌های `backend/**` → rules در `backend/` + `share/`
- فایل‌های `frontend/**` → rules در `frontend/` + `share/`
- سایر فایل‌ها → فقط `share/` و ruleهای مرتبط با همان مسیر

