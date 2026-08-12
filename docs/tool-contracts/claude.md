# قرارداد خروجی Claude Code

قرارداد emitter برای تولید artifactهای بومی Claude Code از IR Aegis.

تاریخ بررسی: ۱۲ اوت ۲۰۲۶.

---

## مستندات رسمی

| صفحه | لینک | خلاصه |
|---|---|---|
| Features overview | https://code.claude.com/docs/en/features-overview | چه زمانی CLAUDE.md، rules، skills، subagents. CLAUDE.md برای always-on؛ skill برای on-demand؛ subagent برای isolation. هدف CLAUDE.md زیر ۲۰۰ خط. |
| Memory / CLAUDE.md / rules | https://code.claude.com/docs/en/memory | `CLAUDE.md` هر جلسه لود می‌شود. `.claude/rules/*.md` ماژولار؛ با `paths` فقط هنگام کار روی فایل مطابق. |
| Skills | https://code.claude.com/docs/en/skills | `SKILL.md` طبق Agent Skills + فیلدهای اضافه Claude (`paths`, `disable-model-invocation`, `context: fork`, ...). `/skill-name` یا auto. |
| Subagents | https://code.claude.com/docs/en/sub-agents | `.claude/agents/<name>.md`. Frontmatter غنی: `tools`, `model`, `skills` preload, `permissionMode`. |
| Directory layout | https://code.claude.com/docs/en/claude-directory | نقشه `.claude/` و `~/.claude/`. |
| Workflows | https://code.claude.com/docs/en/workflows | Dynamic workflows = اسکریپت JS برای ارکستراسیون تعداد زیاد subagent. برای DAG تیمی Aegis لازم نیست؛ skill+subagent کافی است. |
| Agent Skills spec | https://agentskills.io | هستهٔ قابل حمل `name`/`description`. |

### خلاصه CLAUDE.md و Rules

- مسیر پروژه: `./CLAUDE.md` یا `./.claude/CLAUDE.md`
- همیشه در شروع جلسه لود می‌شود؛ context است نه enforcement سخت
- هدف: زیر ۲۰۰ خط؛ دستور build، قراردادها، «always/never»
- `.claude/rules/*.md` بازگشتی؛ بدون `paths` مثل CLAUDE.md لود می‌شود
- با `paths` فقط وقتی فایل مطابق خوانده شود:

```yaml
---
paths:
  - "backend/**/*.py"
---
```

- Claude `AGENTS.md` را نمی‌خواند مگر با `@AGENTS.md` داخل CLAUDE.md یا symlink
- Managed policy سازمانی جدا از پروژه است

مقایسه رسمی:

| | CLAUDE.md | `.claude/rules/` | Skill |
|---|---|---|---|
| لود | هر جلسه | هر جلسه یا با path | روی تقاضا |
| محدوده | کل پروژه | قابل محدود به path | کار خاص |
| مناسب | قرارداد هسته | راهنمای زبان/پوشه | مرجع و فرآیند |

### خلاصه Skills

- مسیر پروژه: `.claude/skills/<folder>/SKILL.md`
- Frontmatter توصیه‌شده: `description` (ترکیب با `when_to_use` تا ۱۵۳۶ کاراکتر در listing)
- `name` اختیاری است (default = نام پوشه)
- فیلدهای مفید Aegis: `paths`, `disable-model-invocation`, `user-invocable`, `metadata`
- `user-invocable: false` برای دانش پس‌زمینه که نباید در منوی `/` باشد
- Commands قدیمی `.claude/commands/` هنوز کار می‌کنند؛ skill ارجح است
- پوشه می‌تواند `references/` و `scripts/` داشته باشد

### خلاصه Subagents

- مسیر: `.claude/agents/<name>.md`
- الزامی: `name`, `description`
- اختیاری مهم: `tools`, `disallowedTools`, `model` (`haiku`/`sonnet`/`opus`/`inherit`), `skills` (preload متن کامل), `permissionMode`, `maxTurns`, `memory`, `background`
- architect/reviewer: ابزار بدون Write/Edit
- می‌توان skillهای مرتبط را در `skills:` preload کرد

---

## نگاشت Kind → Artifact

| Kind Aegis | Artifact Claude | مسیر | Frontmatter / رفتار |
|---|---|---|---|
| `rule` | Path-scoped rule | `.claude/rules/<id>.md` | `paths` از `applies_to`؛ اگر glob ندارد بدون paths (همیشه) |
| `policy` | Rule یا بند CLAUDE.md | `.claude/rules/<id>.md` | سیاست بدون glob → بدون `paths` |
| `principle` | CLAUDE.md (گلوله کوتاه) | `.claude/CLAUDE.md` | فقط عنوان+یک خط؛ متن کامل در skill اگر طولانی است |
| `architecture` | CLAUDE.md یک خط + Skill جزئیات | skill با `paths` | CLAUDE.md را باد نکنید |
| `workflow` | Skill | `.claude/skills/<id>/SKILL.md` | فرآیند دستی: `disable-model-invocation: true` تا `/name` |
| `skill` | Skill | `.claude/skills/<id>/SKILL.md` | `description` + `paths` |
| `reference` | Skill | `.claude/skills/<id>/SKILL.md` | `user-invocable: false` اگر فقط مرجع پس‌زمینه است |
| `agents` | Subagent | `.claude/agents/<id>.md` | `tools` از permissions؛ `skills` = idهای دانش دامنه (اختیاری، نه همه ۴۳ تا) |

Workflow رسمی DAG: skill با مراحل که صریحاً بگوید کدام subagent را صدا کند. Dynamic workflows JS فقط اگر ارکستراسیون در مقیاس بزرگ لازم شود — پیش‌فرض Aegis نیست.

---

## طرح فایل خروجی

```
.claude/
├── CLAUDE.md                 # یا CLAUDE.md در ریشه پروژه
├── rules/
│   ├── shared-rule-precedence.md
│   ├── backend-security-security.md
│   └── frontend-ui-ux-accessibility.md
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
```

اگر مخزن `AGENTS.md` هم برای Cursor/Kilo دارد:

```markdown
@AGENTS.md

## Claude Code
Detailed rules live in `.claude/rules/`. Skills in `.claude/skills/`.
```

---

## Schema فایل‌ها

### Rule `.claude/rules/<id>.md`

```yaml
---
paths:
  - "backend/**/views.py"
  - "backend/**/serializers.py"
---

# API & REST Rules

<body>
```

بدون `paths` = همیشه لود. نام فایل توصیفی باشد.

### CLAUDE.md

```markdown
# Aegis Project

## Always
- Follow shared engineering principles (SSOT, SoC, DRY, KISS, YAGNI).
- Never commit secrets. Use environment variables.

## Architecture (pointers)
- Django: app-based; business logic in services. Details: skill `backend-architecture-django-architecture`
- Vue: atomic design + SoC. Details: skill `frontend-architecture-atomic-design`

## Agents
Delegate implementation to `backend` / `frontend`. Review via `reviewer`. Architecture via `architect`.
```

زیر ۲۰۰ خط. فهرست کامل ۵۵ سند را اینجا نگذارید.

### Skill `SKILL.md`

```yaml
---
name: frontend-state-pinia
description: Pinia store patterns for Vue 3. Use when editing stores or global frontend state.
paths:
  - "frontend/src/stores/**/*.js"
  - "frontend/src/**/*.vue"
---

# Pinia

<body>
```

برای workflow دستی:

```yaml
---
name: shared-rules-audit-checklist
description: Audit knowledge and generated rules for completeness.
disable-model-invocation: true
---
```

### Subagent

```yaml
---
name: backend
description: Implement Django REST APIs, models, serializers, and tests. Use when the task is backend Python.
tools: Read, Grep, Glob, Write, Edit
model: sonnet
---

You are **Backend Engineer Agent**. ...
```

Architect / reviewer بدون Write/Edit:

```yaml
---
name: reviewer
description: Security and standards review after implementation. Use to audit diffs for policy, security, and architecture.
tools: Read, Grep, Glob
model: opus
---
```

Preload فقط skillهای کلیدی همان نقش، نه کل دامنه — متن کامل skill وارد context subagent می‌شود.

---

## فاصله با emitter فعلی

`emitters/claude.py` امروز:

- `rule|principle|reference|policy|skill` همه را skill می‌کند → rules همیشه-روشن نمی‌شوند و CLAUDE.md شلوغ می‌شود
- `.claude/rules/` تولید نمی‌کند
- `architecture` و `workflow` را skip می‌کند
- CLAUDE.md فقط گلوله‌های summary است (نزدیک به هدف، اما باید کوتاه و اشاره‌ای بماند)
- agent `tools` را به‌صورت رشته می‌نویسد (با docs سازگار است)
- `readonly` معادل Claude، لیست `tools` محدود است — این بخش نسبتاً درست است

هدف: rules جدا، skills جدا، CLAUDE.md کوتاه، architecture/workflow به‌صورت skill.

---

## قواعد کیفیت

1. هر چیزی که «always do / never do» است → rule یا CLAUDE.md، نه skill.
2. مرجع طولانی → skill؛ در CLAUDE.md فقط pointer.
3. CLAUDE.md را با لیست ۵۵ سند پر نکنید.
4. `paths` روی rule معادل `applies_to` است.
5. Subagent برای دانش اجرایی نسازید؛ برای نقش و isolation بسازید.
6. Claude `AGENTS.md` را پیش‌فرض نمی‌خواند؛ یا CLAUDE.md بنویسید یا import کنید.
