---
id: frontend-architecture-atomic-design
kind: architecture
domain: frontend
category: architecture
generated_at: 2026-06-11T20:40:16.250653+00:00
---

# Atomic Design

---
title: Atomic Design
summary: Atomic Design principles for organizing UI components into atoms, molecules, organisms, templates, and pages
domain: frontend
category: architecture
applies_to:
  - "frontend/src/**/*.vue"
  - "frontend/src/**/*.js"
priority: 50
kind: architecture
---

# Atomic Design Principles

## اصول Atomic Design

### Atoms (اتم‌ها)
کوچکترین اجزای UI که قابل تقسیم نیستند.

**مثال:** Button, Input, Label, Icon

**قوانین:**
- باید کاملاً مستقل و قابل استفاده مجدد باشند
- نباید وابستگی به سایر کامپوننت‌ها داشته باشند
- باید props محدود و واضح داشته باشند

### Molecules (مولکول‌ها)
ترکیب چند اتم برای ایجاد یک واحد عملکردی.

**مثال:** SearchBox (Input + Button), FormField (Label + Input)

**قوانین:**
- باید از atoms ساخته شوند
- باید یک مسئولیت واحد داشته باشند
- باید قابل استفاده مجدد در context‌های مختلف باشند

### Organisms (ارگانیسم‌ها)
ترکیب molecules و atoms برای ایجاد بخش‌های پیچیده UI.

**مثال:** Header, Table, Navigation

**قوانین:**
- باید از molecules و atoms ساخته شوند
- باید بخش‌های مستقل و قابل استفاده مجدد باشند
- می‌توانند state محلی داشته باشند

### Templates (الگوها)
ساختار صفحه بدون محتوای واقعی.

**قوانین:**
- باید layout و ساختار را تعریف کنند
- باید از organisms, molecules و atoms ساخته شوند
- باید wireframe-like باشند

### Pages (صفحات)
نمونه‌های واقعی از templates با محتوای واقعی.

**قوانین:**
- باید از templates ساخته شوند
- باید محتوای واقعی داشته باشند
- برای تست و مستندسازی استفاده می‌شوند

## استراتژی تقسیم کامپوننت‌ها

- از کوچک 
