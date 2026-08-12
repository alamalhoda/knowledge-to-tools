# قرارداد خروجی Kilo

قرارداد emitter برای تولید artifactهای بومی Kilo Code از IR Aegis.

تاریخ بررسی: ۱۲ اوت ۲۰۲۶.

---

## مستندات رسمی

| صفحه | لینک | خلاصه |
|---|---|---|
| Skills | https://kilo.ai/docs/customize/skills | Agent Skills: پوشه با `SKILL.md`. Discovery فقط metadata؛ بار کامل روی تقاضا. `name` باید با پوشه یکی باشد. |
| Custom Rules | https://kilo.ai/docs/customize/custom-rules | دستورالعمل پایدار. فایل markdown که از `instructions` در `kilo.jsonc` اشاره می‌شود. معمولاً `.kilo/rules/*.md`. |
| Custom Instructions | https://kilo.ai/docs/customize/custom-instructions | لایه‌ها: prompt هر ایجنت، `AGENTS.md` / `CLAUDE.md` / `CONTEXT.md`، instructions در config، AGENTS.md تو در تو. |
| Custom Modes / Agents | https://kilo.ai/docs/customize/custom-modes | در CLI/extension جدید، mode همان agent است. فایل `.kilo/agents/<name>.md` با YAML frontmatter یا کلید `agent` در `kilo.jsonc`. |
| Custom Subagents | https://kilo.ai/docs/customize/custom-subagents | ایجنت با `mode: subagent`. ایزوله؛ فراخوانی با Task tool یا `@name`. |
| Agent Permissions | https://kilo.ai/docs/customize/agent-permissions | `allow` / `ask` / `deny` با glob. last-match-wins. |
| Agent Skills spec | https://agentskills.io | استاندارد باز مشترک با Cursor و Claude. |

### خلاصه Skills

- مسیر پروژه: `.kilo/skills/<name>/SKILL.md`
- مسیر کاربر: `~/.kilo/skills/`
- سازگاری: `.agents/skills/`، و `.claude/skills/` اگر Claude compatibility روشن باشد
- Frontmatter الزامی: `name` (max 64، lowercase/hyphen، برابر نام پوشه)، `description` (max 1024)
- اختیاری: `license`, `compatibility`, `metadata`
- Discovery: فقط name/description/path در system prompt
- تصمیم استفاده: LLM روی `description`؛ keyword matching نیست
- پروژه بر global با نام یکسان اولویت دارد
- `skills.paths` و `skills.urls` در `kilo.jsonc`
- پوشهٔ mode-specific دیگر وجود ندارد؛ با description محدود کنید
- `!`command`` در بدنه فقط برای skillهای trusted اجرا می‌شود؛ skill پروژه untrusted است

### خلاصه Rules / Instructions

- Rules متن markdown هستند، نه `.mdc`
- اتصال از `kilo.jsonc`: `"instructions": [".kilo/rules/*.md"]`
- Global: `instructions` در `~/.config/kilo/kilo.jsonc`
- Auto-discover ریشه: `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`
- AGENTS.md زیردایرکتوری وقتی Read روی آن مسیر می‌رود تزریق می‌شود
- Project instructions بر global اولویت دارد
- سازگاری قدیمی: `.kilocode/rules/`

### خلاصه Agents

- مسیر: `.kilo/agents/<name>.md` یا `.kilo/agent/` یا کلید `agent` در `kilo.jsonc`
- Frontmatter مهم: `description`, `mode` (`primary` | `subagent` | `all`), `permission`, `model`, `color`, `steps`, `hidden`, `disable`
- بدنه markdown = system prompt
- `mode: primary` در picker؛ `subagent` فقط Task/`@`
- مجوز: `edit`, `bash`, `read`, `task`, `webfetch`, ...
- architect/reviewer بدون edit: `permission.edit: deny`

Kilo **workflow native** و **architecture native** جدا ندارد. فرآیند را skill کنید؛ blueprint را skill یا instructions.

---

## نگاشت Kind → Artifact

| Kind Aegis | Artifact Kilo | مسیر | نکات |
|---|---|---|---|
| `rule` | Custom Rule | `.kilo/rules/<id>.md` + ثبت در `instructions` | قید پایدار؛ همه مدل‌ها در تعامل پروژه |
| `policy` | Custom Rule | `.kilo/rules/<id>.md` | سیاست سازمانی در instructions |
| `principle` | `AGENTS.md` (خلاصه) + در صورت نیاز rule | ریشه `AGENTS.md` | اصل کوتاه همیشه-روشن |
| `architecture` | Skill | `.kilo/skills/<id>/SKILL.md` | description باید بگوید «when designing / structuring» |
| `workflow` | Skill | `.kilo/skills/<id>/SKILL.md` | فرآیند تکرارشونده؛ description با triggerهای کاربر |
| `skill` | Skill | `.kilo/skills/<id>/SKILL.md` | نگاشت مستقیم |
| `reference` | Skill با `references/` | `.kilo/skills/<id>/SKILL.md` | جزئیات را از SKILL.md اصلی جدا کنید |
| `agents` | Agent markdown | `.kilo/agents/<id>.md` | `mode: all` یا primary برای نقش‌های کاربر؛ reviewer می‌تواند `all` با edit deny باشد |

Workflow رسمی DAG: skill ارکستراسیون (مراحل + ایجنت مسئول هر مرحله) **و** ایجنت‌ها با `description` مناسب برای Task tool. پوشهٔ ساختگی `workflows/` که Kilo نمی‌خواند تولید نکنید مگر به‌عنوان منبع انسانی داخل skill.

---

## طرح فایل خروجی

```
.kilo/
├── rules/
│   ├── shared-rule-precedence.md
│   ├── backend-security-security.md
│   └── ...
├── skills/
│   ├── frontend-state-pinia/
│   │   └── SKILL.md
│   └── backend-api-flow/
│       └── SKILL.md
└── agents/
    ├── architect.md
    ├── backend.md
    ├── frontend.md
    └── reviewer.md
kilo.jsonc
AGENTS.md
```

### `kilo.jsonc` حداقلی

```jsonc
{
  "instructions": [".kilo/rules/*.md"],
  "skills": {
    "paths": [".kilo/skills"]
  }
}
```

ایجنت‌ها از فایل markdown کشف می‌شوند؛ تکرار کامل در `agent` کلید لازم نیست مگر override مدل.

---

## Schema فایل‌ها

### Rule `.md`

Markdown با هدر و لیست. Frontmatter Kilo برای rules الزامی نیست.

```markdown
# Security Rules

- validation فقط در Serializer
- secrets فقط در environment variables
```

در `instructions` glob شود تا بار شود.

### Skill `SKILL.md`

```yaml
---
name: frontend-state-pinia
description: Pinia store patterns for Vue 3. Use when creating or editing Pinia stores, global state, or frontend/src/stores.
---

# Pinia

<body>
```

`name` = نام پوشه. فیلدهای `id`/`kind`/`domain` در frontmatter استاندارد Kilo نیستند؛ اگر لازم است داخل `metadata` بگذارید:

```yaml
metadata:
  aegis_kind: skill
  aegis_domain: frontend
```

### Agent `.md`

```yaml
---
description: Backend Django/API implementation. Use for REST endpoints, models, serializers, tests.
mode: primary
color: "#3B82F6"
permission:
  edit: allow
  bash: deny
  read: allow
---

You are **Backend Engineer Agent**. ...
```

Reviewer:

```yaml
---
description: Quality and security review. Use after implementation to audit standards, security, and architecture consistency.
mode: all
permission:
  edit: deny
  bash: deny
  read: allow
---
```

`steps` را در IR نگذارید مگر قرارداد جدا برای سقف هزینه؛ مستندات Kilo آن را اختیاری می‌داند.

---

## فاصله با emitter فعلی

`emitters/kilo.py` امروز:

- skill می‌سازد اما frontmatter `id`/`kind`/`domain` دارد، نه `name`/`description` الزامی spec
- پوشه‌های `workflows/` و `architecture/` می‌سازد که Kilo native نیست
- `AGENTS.md` خلاصه می‌نویسد (مفید) اما rules را به `instructions` وصل نمی‌کند
- `kilo.jsonc` تولید نمی‌کند
- agent frontmatter فیلدهای غیرمستند مثل `context:` و `steps: 30` دارد

هدف: skill مطابق spec، rules در `.kilo/rules` + `kilo.jsonc`، architecture/workflow به‌صورت skill، agent مطابق custom-modes.

---

## قواعد کیفیت

1. بدون `name`+`description` معتبر، skill لود نمی‌شود.
2. Rule را skill نکنید اگر باید در هر تعامل پروژه اعمال شود.
3. `description` را با زبان درخواست کاربر بنویسید («REST API»، «Pinia store») نه فقط شناسه داخلی.
4. Skill پروژه `!`command`` نداشته باشد؛ untrusted است.
5. ایجنت بدون `description` خوب توسط Orchestrator/Task انتخاب نمی‌شود.
