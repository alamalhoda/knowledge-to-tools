---
id: shared-engineering-principles
kind: principle
domain: shared
category: engineering-principles.mdc
generated_at: 2026-06-09T20:12:15.500247+00:00
---

# Engineering Principles

---
title: Engineering Principles
summary: Universal engineering principles for maintainable code across the project
domain: shared
category: engineering-principles.mdc
applies_to:
priority: 80
kind: principle
---

# Engineering Principles (Shared)

این اصول برای همه بخش‌ها (backend/frontend/docs/scripts) معتبر هستند.

## Core Principles

- **SSOT:** هر منطق یا قانون باید یک منبع یکتا داشته باشد.
- **Separation of Concerns:** UI/transport, business logic, data access را جدا نگه دار.
- **DRY:** از تکرار منطق پرهیز کن؛ استخراج helper/service زمانی که تکرار دیده می‌شود.
- **KISS:** ساده‌ترین طراحی درست را انتخاب کن.
- **YAGNI:** قابلیت اضافی بدون نیاز فعلی اضافه نکن.
- **Minimize Change Impact:** تغییرات کوچک، قابل بازبینی، و با اثر جانبی محدود انجام بده.
- **Explicitness:** قراردادها (ورودی/خروجی/خطا) واضح باشند، نه ضمنی.

## Decision Rules

- اگر بین دو قاعده conflict دیدی، اولویت با rule تخصصی همان دامنه است.
- اگر rule مبهم بود، سؤال بپرس؛ حدس نزن.

