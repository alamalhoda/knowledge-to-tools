---
title: Best Practices
summary: Python Best Practices — Type hints، context managers، dataclass، exception handling
domain: backend
category: python
applies_to:
  - "backend/**/*.py"
priority: 50
kind: skill
---

# Python Best Practices

## الزامات

* Type hints الزامی برای توابع عمومی
* Context manager برای resource (file، connection، lock)
* `dataclass` برای DTO
* Exception handling صریح (نه bare `except:`)

## مثال

❌ نادرست:

```python
def f(x): return x[0]
```

✅ درست:

```python
def get_first(items: list[str]) -> str:
    return items[0]
```
