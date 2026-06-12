# knowledge-to-tools / تبدیل دانش به ابزار

**تبدیل دانش پروژه‌ای به ابزار و تنظیمات هوش مصنوعی، به‌صورت خودکار، بدون وابستگی به ابزار خاص.**

**Convert project knowledge into AI agent tools automatically, in a tool-agnostic way.**

---

## 🎯 هدف / Goal

هدف این پروژه، تبدیل مجموعه‌ای از دانش فنی، روندها، قوانین و الگوهای یک تیم نرم‌افزاری، به فایل‌های پیکربندی قابل استفاده در ابزارهای هوش مصنوعی (مانند Kilo، Cursor، OpenCode) است.

این کار را با تعریف یک **نماد میانی (IR)** انجام می‌دهد، که هیچ وابستگی به ابزار خاصی ندارد و سپس به‌صورت خودکار به خروجی‌های ضروری برای هر ابزار تبدیل می‌شود.

The goal of this project is to convert a team's technical knowledge, workflows, rules, and patterns into **AI-agent configuration files** (for Kilo, Cursor, OpenCode, etc.).

This is achieved via a **tool-agnostic Intermediate Representation (IR)** that gets compiled and emitted into tool-specific artifacts automatically.

---

## 🏗️ معماری / Architecture

```
Knowledge (Markdown/JSON)
        │
        ▼
   IR Compiler  ──►  Validator  ──►  Emitters (Kilo / OpenCode / Cursor)
        │
        ▼
  SerializedIRPayload (Runtime-safe)
```

| مرحله/Stage | توضیحات |
|---|---|
| **Knowledge** | دانش پروژه شامل اسناد Markdown، JSONهایی برای Agents، Workflows، Capabilities |
| **IR Compiler** | کامپایلر تعیین‌کننده که knowledge را به یک ساختار استاندارد (IR) تبدیل می‌کند |
| **Validator** | بررسی صحت IR (عدم تکرار ID، حلقه‌های وابستگی، صحت مراجع) |
| **Emitters** | تبدیل IR به فرمت‌های خروجی هر ابزار (بدون تغییر هسته اصلی) |

---

## 📥 ورودی‌ها / Inputs

ورودی‌های کلیدی از پوشه‌های زیر خوانده می‌شوند:

```
knowledge-to-tools/
├── knowledge/
│   ├── backend/core/       # دانش فنی بک‌اند
│   ├── frontend/core/      # دانش فنی فرانت‌اند
│   └── shared/             # دانش مشترک
├── agents/*.json           # تعریف هوش‌مصنوعی‌ها (Architect، Backend، Reviewer...)
├── workflows/index.json    # فرمول‌های کاری pipeline
└── capabilities/index.json # قابلیت‌های تکمیلی
```

### ساختار یک دانش‌نامه (Knowledge Doc)

```markdown
# عنوان دانش‌نامه

> توضیح مختصر حوزه و کاربرد

## قوانین کلیدی
1. ...
2. ...

## الگوهای جایگزین
- ...

## خطاهای رایج
- ...
```

---

## ⚙️ فرآیند تولید / Build Process

```bash
# نصب وابستگی‌ها (در صورت نیاز)
pip install -r requirements.txt  # اگر موجود باشد

# تولید خروجی
python۳ pipeline/generate.py
```

**مراحل داخلی generate.py:**

1. بارگذاری `knowledge/index.json` و فایل‌های JSON agents
2. بارگذاری متن خام اسناد دانش
3. کامپایل IR با `IRCompiler`
4. اعتبارسنجی با `IRValidator` (در صورت خطا فوراً متوقف می‌شود)
5. ذخیره `.ai/ir/ir_compiled.json`
6. امی‌ت (emit) فایل‌های هر ابزار:
   - **Kilo** → `.kilo/`
   - **OpenCode** → `.opencode/`
   - **Cursor** → `.cursor/`

---

## 📤 خروجی‌ها / Outputs

به‌طور خودکار در پوشه‌های زیر تولید می‌شوند:

```
AI-Project-root/
├── .kilo/          # تنظیمات Kilo (agents, skills, workflows)
├── .opencode/      # تنظیمات OpenCode
├── .cursor/        # تنظیمات Cursor
└── .ai/
    └── ir/
        └── ir_compiled.json   # خروجی نهایی IR
```

**ویژگی کلیدی:** می‌توانید تنها امیتر مربوط به یک ابزار خاص را فعال/غیرفعال کنید تا سایر خروجی‌ها تولید نشوند.

---

## 📁 ساختار پروژه / Project Structure

```
knowledge-to-tools/
├── README.md                 # همین فایل
├── agents/                   # تعریف هوش‌های مصنوعی (JSON)
│   ├── architect.json
│   ├── backend.json
│   ├── frontend.json
│   └── reviewer.json
├── capabilities/             # قابلیت‌های سیستم (JSON)
│   └── index.json
├── core/                     # هسته اصلی (Compiler, Bundler, Resolver)
│   ├── compiler.py
│   ├── models.py
│   └── skill_graph.py
├── docs/                     # مستندات فنی
│   └── ARCHITECTURE_REPORT.md
├── emitters/                 # تولیدکننده خروجی هر ابزار
│   ├── kilo.py
│   ├── opencode.py
│   ├── cursor.py
│   └── base.py
├── ir/                       # لایه Intermediate Representation (IR)
│   ├── compiler.py            # کامپایلر
│   ├── validator.py           # اعتبارسنج‌کننده
│   ├── version.py             # نسخه‌بندی IR
│   └── models/                # مدل‌های دیتاکلاس (frozen)
├── knowledge/                # پایگاه دانش فنی پروژه
│   ├── index.json
│   ├── backend/
│   ├── frontend/
│   └── shared/
├── pipeline/                
│   ├── generate.py            # نقطه ورودی اصلی (CLI)
│   ├── audit.py
│   └── knowledge_index.py
├── planning/                  # انجین برنامه‌ریزی
├── router/                    # مسیریابی درخواست‌ها
├── runtime/                   #mosphere لایتنر و موتورهای اجرایی
├── tests/                     # تست‌های موجودات و آرشیوها
├── workflows/                 # تعریف جریان‌های کاری
│   └── index.json
├── schema/                    # schema‌های اعتبارسنجی
└── .gitignore
```

---

## 🧪 تست‌ها / Testing

```bash
# اجرای تست‌ها
pytest knowledge-to-tools/tests/

# یا با پایتون مستقیم
python -m unittest discover -s knowledge-to-tools/tests
```

تست‌های موجود شامل:
- **IR Snapshots** — بررسی تطبیق خروجی با نمونه‌های ذخیره شده
- **Architecture Integrity** — قطعی‌سنجی معماری (عدم نشت وابستگی بین لایه‌ها)

---

## 🔌 لایه‌های سیستم / System Layers

| لایه/Layer | شرح/Description |
|---|---|
| `knowledge/` | دانش فنی در فرمت Markdown + index.json |
| `ir/` | Intermediate Representation (کامپایلر + مدل‌ها + اعتبارسنج) |
| `core/` | منطق تجميع، تحلیل وابیستگی و تولید گراف مهارت |
| `emitters/` | تبدیل IR به خروجی هر ابزار |
| `pipeline/` | فرآیند end-to-end: ورودی → خروجی |
| `runtime/` | موتورهای زمان اجرا (planning، routing) |

---

## 📝 نکات توسعه / Development Notes

- **هسته‌ی دائری:** لایه `ir/` هیچ وابستگی به ابزار خاصی ندارد و می‌تواند سازه اصلی باقی بماند تا امیترهای جدید اضافه شوند.
- **امضای خطرناک簽名:** حتماً حاصل‌ضرب SHA256 ورودی‌ها را در `ir_compiled.json` بررسی کنید تا از تغییر ناخواسته‌های دانش جلوگیری شود.
- **Migrate Cursor Rules:** اسکریپت `pipeline/migrate_cursor_rules.py` برای توسعه‌دهندگانی که می‌خواهند قوانین Cursor خود را به این ساختار مهاجرت دهند، آماده شده است.

---

## 🚀 شروع سریع / Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/knowledge-to-tools.git
cd knowledge-to-tools

# تنظیم knowledge/ بر اساس پروژه خود
python pipeline/generate.py

# خروجی در پوشه‌های .kilo/، .opencode/، .cursor/ آماده است
```

---

## 🔒 امنیت / Security

- هیچ کلید API یا token داخل این مخزن **نباید** وجود داشته باشد.
- تمام تنظیمات محلی در `.gitignore` قرار بگیرند.

---

## 📄 مجوز / License

[نام مجوز خود را اینجا بنویسید، مثلا MIT]
