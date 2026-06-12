---
id: frontend-architecture-solid
kind: principle
domain: frontend
category: architecture
generated_at: 2026-06-11T20:40:16.251926+00:00
---

# Solid

---
title: Solid
summary: SOLID principles applied to frontend component design and architecture
domain: frontend
category: architecture
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: principle
---

# SOLID Principles

## SRP — Single Responsibility Principle

هر کامپوننت فقط یک دلیل برای تغییر دارد.

**چرا مهم است؟**
افزایش خوانایی، تست‌پذیری و قابلیت استفاده مجدد با تمرکز بر یک مسئولیت.

**قوانین:**
- کامپوننت‌ها باید یک مسئولیت واحد داشته باشند
- منطق نمایش را از منطق تجاری جدا کن
- منطق API را از کامپوننت‌ها جدا کن

## OCP — Open/Closed Principle

باز برای گسترش، بسته برای تغییر.

**چرا مهم است؟**
افزودن قابلیت جدید بدون تغییر کامپوننت‌های تست‌شده.

**قوانین:**
- از configuration objects برای رفتارهای مختلف استفاده کن
- از composition به جای modification استفاده کن
- از props و slots برای گسترش استفاده کن

## LSP — Liskov Substitution Principle

زیرکلاس‌ها باید بدون شکستن رفتار، جایگزین کلاس والد شوند.

**چرا مهم است؟**
تضمین رفتار صحیح در Polymorphism و جلوگیری از باگ‌های runtime.

**قوانین:**
- کامپوننت‌های مشتق شده باید با کامپوننت پایه قابل تعویض باشند
- از props مشترک و سازگار استفاده کن
- از رفتارهای غیرمنتظره در کامپوننت‌های مشتق شده پرهیز کن

## ISP — Interface Segregation Principle

کلاینت‌ها نباید به interface‌هایی که استفاده نمی‌کنند وابسته باشند.

**چرا مهم است؟**
کاهش وابستگی‌های غیرضروری و افزایش انعطاف‌پذیری.

**قوانین:**
- props را به گروه‌های منطقی تقسیم کن
- از props اختیاری به جای props اجباری استفاده کن
- از compo
