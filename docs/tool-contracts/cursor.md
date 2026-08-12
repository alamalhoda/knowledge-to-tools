# قرارداد خروجی Cursor

قرارداد emitter برای تولید artifactهای بومی Cursor از IR Aegis.

تاریخ بررسی: ۱۲ اوت ۲۰۲۶.

---

## مستندات رسمی

| صفحه | لینک | خلاصه |
|---|---|---|
| Rules | https://cursor.com/docs/rules | دستورالعمل پایدار در سطح prompt. چهار نوع: Project (`.cursor/rules/*.mdc`)، User، Team، و `AGENTS.md`. فایل `.md` داخل `rules/` نادیده گرفته می‌شود. |
| Agent Skills | https://cursor.com/docs/skills | بستهٔ قابل حمل طبق استاندارد Agent Skills. پوشه با `SKILL.md`. کشف از `.cursor/skills/` و `.agents/skills/`. بارگذاری پیش‌رونده؛ ایجنت با `description` تصمیم می‌گیرد. |
| Subagents | https://cursor.com/docs/subagents | دستیار ایزوله با context جدا. فایل markdown در `.cursor/agents/`. برای کار موازی و تخصص؛ برای کار تک‌مرحله‌ای skill بهتر است. |
| Customize | https://cursor.com/docs/customize-cursor | مدیریت متمرکز plugins، rules، skills، subagents، commands، hooks. |
| Agent Skills spec | https://agentskills.io | استاندارد باز `SKILL.md`. |

### خلاصه Rules

- مسیر پروژه: `.cursor/rules/**/*.mdc`
- Frontmatter: `description`, `globs`, `alwaysApply`
- چهار حالت فعال‌سازی:

| alwaysApply | description | globs | رفتار |
|---|---|---|---|
| `true` | — | — | همیشه در context |
| `false` | — | دارد | Auto-attach وقتی فایل مطابق glob در context است |
| `false` | دارد | ندارد | ایجنت با description تصمیم می‌گیرد |
| `false` | ندارد | ندارد | فقط با `@rule-name` |

- حداکثر حدود ۵۰۰ خط در هر rule؛ rule بزرگ را بشکنید.
- `AGENTS.md` جایگزین ساده بدون metadata است؛ تو در تو در زیردایرکتوری‌ها اعمال می‌شود.
- اولویت: Team Rules → Project Rules → User Rules.
- Rules روی Cursor Tab اثر ندارند؛ فقط Agent (Chat).

### خلاصه Skills

- مسیر: `.cursor/skills/<folder>/SKILL.md` (همچنین `.agents/skills/`، سازگاری با `.claude/skills/`)
- Frontmatter الزامی: `name` (باید با نام پوشه یکی باشد)، `description`
- اختیاری: `paths` (glob؛ جایگزین legacy `globs`)، `disable-model-invocation`, `metadata`
- پوشه‌های اختیاری: `scripts/`, `references/`, `assets/`
- `/skill-name` برای فراخوانی دستی
- `/migrate-to-skills` فقط ruleهای «Apply Intelligently» را به skill تبدیل می‌کند؛ `alwaysApply` و globدار مهاجرت نمی‌شوند

### خلاصه Subagents

- مسیر: `.cursor/agents/<name>.md` (سازگاری: `.claude/agents/`)
- Frontmatter: `name`, `description`, `model` (`inherit` یا model ID), `readonly`, `is_background`
- بدنه = system prompt
- Built-in: Explore, Bash, Browser
- اگر کار تک‌منظوره است، skill بسازید نه subagent

---

## نگاشت Kind → Artifact

| Kind Aegis | Artifact Cursor | مسیر | Frontmatter پیشنهادی | دلیل |
|---|---|---|---|---|
| `rule` | Project Rule | `.cursor/rules/<id>.mdc` | `alwaysApply: false` + `globs` از `applies_to`؛ اگر glob خالی و `priority >= 80` آنگاه `alwaysApply: true` | قید اجباری باید در context فایل مربوطه باشد |
| `policy` | Project Rule | `.cursor/rules/<id>.mdc` | `alwaysApply: true` اگر glob ندارد؛ وگرنه glob | سیاست سازمانی باید پایدار باشد |
| `principle` | Project Rule | `.cursor/rules/<id>.mdc` | `alwaysApply: true` برای `priority >= 80`؛ وگرنه `description` بدون glob (Agent Decides) | اصل راهنما است؛ اصول shared با اولویت بالا همیشه روشن |
| `architecture` | Skill | `.cursor/skills/<id>/SKILL.md` | `name`, `description`, `paths` از `applies_to` | جزئیات معماری روی تقاضا؛ خلاصه در AGENTS.md |
| `workflow` | Skill | `.cursor/skills/<id>/SKILL.md` | `name`, `description`؛ اگر فرآیند دستی است `disable-model-invocation: true` | فرآیند تکرارشونده، نه قید همیشه-روشن |
| `skill` | Skill | `.cursor/skills/<id>/SKILL.md` | `name`, `description`, `paths` | دانش اجرایی بومی Cursor |
| `reference` | Skill + `references/` | `.cursor/skills/<id>/SKILL.md` و در صورت حجم `references/REFERENCE.md` | `name`, `description` | مرجع نباید context را پر کند |
| `agents` | Subagent | `.cursor/agents/<id>.md` | `name`, `description`, `readonly` از `permissions.edit == false`, `model: inherit` | نقش ایزوله با مجوز |

Workflow رسمی DAG (`workflows/index.json`): یک skill ارکستراسیون با مراحل، که در description بگوید چه زمانی ایجنت‌ها را delegate کند. خود DAG در Cursor native نیست.

---

## طرح فایل خروجی

```
.cursor/
├── rules/
│   ├── shared-rule-precedence.mdc
│   ├── backend-security-security.mdc
│   └── ...
├── skills/
│   ├── frontend-state-pinia/
│   │   └── SKILL.md
│   └── backend-api-flow/          # workflow رسمی
│       └── SKILL.md
└── agents/
    ├── architect.md
    ├── backend.md
    ├── frontend.md
    └── reviewer.md
AGENTS.md                          # فهرست ایجنت‌ها + اصول همیشه-روشن (کوتاه)
```

`AGENTS.md` ریشه پروژه: خلاصهٔ `principle` با `priority >= 80` و فهرست ایجنت‌ها. جزئیات در rules/skills می‌ماند.

---

## Schema فایل‌ها

### Rule `.mdc`

```yaml
---
description: "<domain> <kind>: <summary> — when to apply"
globs: "<comma-separated or YAML list from applies_to>"
alwaysApply: false
---

<markdown body from knowledge, without duplicating huge style guides>
```

قوانین:
- پسوند باید `.mdc` باشد.
- `description` برای حالت Agent Decides الزامی است.
- چند glob: کاما یا لیست YAML.
- بدنه عملی و با مثال؛ زیر ۵۰۰ خط.

### Skill `SKILL.md`

```yaml
---
name: <id>          # lowercase, hyphens, matches folder
description: "<what + when>. Use when working on <domain> <category>."
paths:
  - "<glob from applies_to>"
---

# <title>

## When to Use
...

## Instructions
<body>
```

`name` باید با نام پوشه یکی باشد. `paths` را به‌جای `globs` بنویسید.

### Subagent `.md`

```yaml
---
name: backend
description: Backend Django/API implementation. Delegate when editing backend Python, REST, models, tests.
model: inherit
readonly: false
---

You are **Backend Engineer Agent**. ...
```

`readonly: true` برای architect و reviewer (`edit: false`).

---

## فاصله با emitter فعلی

`emitters/cursor.py` امروز:

- فقط `rule|principle|reference|policy` را `.mdc` می‌کند
- `skill`, `architecture`, `workflow` را دور می‌ریزد
- subagent می‌سازد اما بدون `readonly` و بدون `description` غنی برای delegation
- skill تولید نمی‌کند
- `AGENTS.md` ریشه را از این emitter نمی‌نویسد (Kilo می‌نویسد)

این قرارداد خروجی هدف است؛ emitter باید به آن برسد.

---

## قواعد کیفیت

1. Rule با glob خالی و اولویت پایین → `description` بدهید تا Agent Decides شود، نه alwaysApply برای همه.
2. Skill بدون `description` مشخص کشف نمی‌شود.
3. Subagent برای «چگونه Vue بنویس» نسازید؛ آن skill است.
4. `reference` را rule نکنید؛ context را باد می‌کند.
5. محتوای rule را از روی دانش کپی کنید اما frontmatter را بومی Cursor کنید؛ فیلدهای IR مثل `kind` داخل frontmatter Cursor نروند مگر در بدنه به‌صورت متن.
