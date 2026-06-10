---
id: shared-offline-no-cdn-policy
kind: policy
domain: shared
category: offline-no-cdn-policy.mdc
generated_at: 2026-06-10T16:55:23.988777+00:00
---

# Offline No Cdn Policy

---
title: Offline No Cdn Policy
summary: جلوگیری از وابستگی به CDN اینترنتی؛ استفاده از نسخه محلی/آفلاین برای فونت، آیکون و اسکریپت
domain: shared
category: offline-no-cdn-policy.mdc
applies_to:
  - "frontend/**/*.html"
  - "frontend/**/*.vue"
  - "frontend/**/*.css"
  - "frontend/**/*.js"
priority: 50
kind: policy
---

# سیاست آفلاین – بدون CDN (Shared)

این پروژه برای runtime به هیچ CDN اینترنتی وابسته نیست. وابستگی جدید به CDN اضافه نکن.

## قوانین اجباری

- **فونت‌ها:** از فایل‌های محلی در `public/fonts/` استفاده کن. لینک به `fonts.googleapis.com` یا `fonts.gstatic.com` اضافه نکن.
- **آیکون‌ها / Font Awesome:** از پوشه محلی `public/fontawesome-pro-7.1.0-web/` استفاده کن. پکیج npm یا اسکریپت از CDN (مثل unpkg، jsdelivr، cdnjs) اضافه نکن.
- **CSS/JS خارجی:** اسکریپت یا استایل از CDN (مثل `cdn.tailwindcss.com`, `unpkg.com`, `jsdelivr.net`) لود نکن. در صورت نیاز، فایل را دانلود کن و در `public/` قرار بده و به مسیر محلی لینک بده.
- **تصاویر:** از مسیرهای محلی (`/images/...` یا `public/images/`) استفاده کن؛ URL خارجی (مثل دامنه‌های third‑party) برای assetهای ضروری UI اضافه نکن.

## الگوی درست

- لینک استایل/فونت: `href="/fonts/..."` یا `href="/fontawesome-pro-7.1.0-web/..."`
- تصویر: `src="/images/..."` یا از `public/` سرو شده

## الگوی ممنوع

- `href="https://fonts.googleapis.com/..."`
- `src="https://cdn..../..."` برای فونت/آیکون/کتابخانه ضروری UI
- وابستگی runtime به هر دامنه خارجی برای منابع ضروری صفحه

## استثناها

- لینک‌های تعاملی کاربر (مثل `https://t.me/...` برای باز 
