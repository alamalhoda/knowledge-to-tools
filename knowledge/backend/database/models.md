---
title: Models
summary: Database Rules — Migrations، model conventions، transactions، Django ORM
domain: backend
category: database
applies_to:
  - "backend/**/models.py"
  - "backend/**/migrations/*.py"
priority: 50
kind: rule
---

# Database Rules (Django ORM)

## Migrations

همیشه migration بساز؛ هرگز دیتابیس را دستی تغییر نده:

```bash
python manage.py makemigrations khodroban
python manage.py migrate
```

## Primary Key (id)

* نام فیلد کلید اصلی برای همه مدل‌ها «id» باشد (به‌جز مواردی که PK همان رابطه OneToOne است، مثل UserProfile).
* نوع PK:
  * **BigAutoField**: برای جدول‌هایی که احتمال رشد زیاد رکورد دارند . محدوده امن برای اعداد بزرگ.
  * **AutoField**: برای جدول‌های مرجع کوچک . کافی برای تعداد محدود رکورد.
  * **UUIDField**: برای موجودیت‌هایی که نیاز به شناسه یکتا در سطح توزیع‌شده یا عدم پیش‌بینی‌پذیری دارند.
  *  استفاده از انواع مختلف مشکلی ایجاد نمی‌کند؛ هر مدل با توجه به نیازش انتخاب شود.
* همه روابط بین جدول‌ها بر اساس FK مبتنی بر id (نه to_field روی فیلد دیگر).

## Model Conventions

* `related_name` معنی‌دار
* `on_delete=PROTECT` برای foreign keyهای حیاتی (مرجع/کاربر)؛ `CASCADE` برای داده‌های وابسته به موجودیت والد (مثلاً سرویس به خودرو).
* `TextChoices` / `IntegerChoices` برای enum
* `db_index=True` برای فیلدهای پرجستجو
* `Meta.indexes` و `Meta.constraints`

❌ نادرست:

```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
status = models.CharField(max_length=20)
```

✅ درست:

```python
class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "در انتظار"
    PAID = "PAID", "پرداخت شده"

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["-created_at"]),
        ]
```

## Transactions

```python
from django.db import transaction

@transaction.atomic
def transfer_balance(from_profile, to_profile, amount):
    from_profile.balance -= amount
    from_profile.save()
    to_profile.balance += amount
    to_profile.save()
```
