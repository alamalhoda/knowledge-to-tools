# قرارداد خروجی OpenCode

قرارداد emitter برای تولید artifactهای بومی OpenCode از IR Aegis.

تاریخ بررسی: ۱۲ اوت ۲۰۲۶.

---

## مستندات رسمی

| صفحه | لینک | خلاصه |
|---|---|---|
| Rules | https://opencode.ai/docs/rules | دستورالعمل پایدار عمدتاً از `AGENTS.md`. سازگاری با `CLAUDE.md`. `instructions` در `opencode.json` برای فایل‌های اضافه. |
| Agent Skills | https://opencode.ai/docs/skills | `SKILL.md` در `.opencode/skills/<name>/`. Frontmatter فقط `name`, `description`, `license`, `compatibility`, `metadata`. بار با tool `skill`. |
| Agents | https://opencode.ai/docs/agents | Primary (Tab) و subagent (`@` یا Task). فایل `.opencode/agents/<name>.md` یا کلید `agent` در `opencode.json`. |
| Commands | https://opencode.ai/docs/commands | پرامپت تکرارشونده در `.opencode/commands/<name>.md`. برای workflow دستی شبیه slash command. |
| Config | https://opencode.ai/docs/config | `opencode.json`: `agent`, `instructions`, `permission`, schema `https://opencode.ai/config.json`. |
| Agent Skills spec | https://agentskills.io | هسته مشترک. |

### خلاصه Rules / AGENTS.md

- فایل اصلی: `AGENTS.md` در ریشه پروژه
- Global: `~/.config/opencode/AGENTS.md`
- `/init` آن را از روی ریپو می‌سازد/بهبود می‌دهد
- اولویت کشف: `AGENTS.md` محلی بر `CLAUDE.md`؛ سپس global OpenCode؛ سپس `~/.claude/CLAUDE.md`
- اگر هر دو `AGENTS.md` و `CLAUDE.md` باشند فقط `AGENTS.md` استفاده می‌شود
- `opencode.json` → `"instructions": ["docs/*.md", ".cursor/rules/*.md"]` فایل‌های اضافه را با AGENTS.md ترکیب می‌کند
- OpenCode `@file` داخل AGENTS.md را خودکار expand نمی‌کند؛ یا `instructions` یا در متن بگویید با Read لود کند

OpenCode **`.mdc` / `.opencode/rules/` بومی** ندارد. قید پایدار = AGENTS.md + instructions.

### خلاصه Skills

- مسیر: `.opencode/skills/<name>/SKILL.md`
- همچنین می‌خواند: `.claude/skills/`, `.agents/skills/`
- Frontmatter شناخته‌شده **فقط**: `name` (الزامی)، `description` (الزامی، ۱–۱۰۲۴)، `license`, `compatibility`, `metadata` (map رشته)
- فیلد ناشناخته ignore می‌شود (`kind`, `id`, `paths` در top-level اثر ندارند)
- `name`: regex `^[a-z0-9]+(-[a-z0-9]+)*$`، ۱–۶۴، برابر نام پوشه
- ایجنت فقط فهرست name+description را در tool `skill` می‌بیند؛ محتوا با `skill({ name })` لود می‌شود
- مجوز: `permission.skill` با `allow`/`deny`/`ask`؛ قابل override per-agent
- برای مخفی کردن از مدل: deny یا disable tool `skill`

V2 docs فیلدهای `slash` و `metadata.opencode/autoinvoke` را هم ذکر می‌کند؛ قرارداد Aegis روی فیلدهای پایدار v1 بالا می‌ماند مگر emitter جدا برای V2.

### خلاصه Agents

- مسیر markdown: `.opencode/agents/<name>.md` — نام فایل = نام ایجنت
- یا JSON در `opencode.json` → `agent.<id>`
- Frontmatter: `description` (الزامی برای انتخاب)، `mode` (`primary`|`subagent`|`all`، default `all`)، `model`, `temperature`, `permission`, `steps`, `hidden`, `color`, `top_p`
- بدنه = system prompt
- Built-in primary: Build, Plan
- Built-in subagent: General, Explore, Scout
- مجوز: `edit`, `bash`, `read`, `skill`, `task`, `webfetch`, ...
- `tools` منسوخ است؛ از `permission` استفاده کنید
- Markdown ارجح است برای prompt بلند

### خلاصه Commands

- `.opencode/commands/<name>.md` → `/name`
- برای workflow که کاربر صریحاً اجرا می‌کند (مثل audit checklist)
- می‌تواند `agent` و `subtask` داشته باشد

---

## نگاشت Kind → Artifact

| Kind Aegis | Artifact OpenCode | مسیر | نکات |
|---|---|---|---|
| `rule` | Instructions file + اشاره در config | `.opencode/instructions/<id>.md` و `instructions` glob | یا بخش فشرده در AGENTS.md برای اولویت بالا |
| `policy` | AGENTS.md + instructions | همان | سیاست همیشه در context ریشه |
| `principle` | AGENTS.md | `AGENTS.md` | گلوله‌های کوتاه |
| `architecture` | AGENTS.md pointer + Skill | skill برای جزئیات | AGENTS.md را با blueprint کامل پر نکنید |
| `workflow` | Skill یا Command | skill پیش‌فرض؛ command اگر باید `/name` باشد | DAG رسمی = skill ارکستراسیون |
| `skill` | Skill | `.opencode/skills/<id>/SKILL.md` | نگاشت مستقیم |
| `reference` | Skill | `.opencode/skills/<id>/SKILL.md` | on-demand از طریق skill tool |
| `agents` | Agent markdown | `.opencode/agents/<id>.md` | نه JSON جدا اگر markdown پشتیبانی می‌شود |

`paths` روی skill در OpenCode (مستندات فعلی) تفسیر نمی‌شود. محدوده فایل را در `description` بنویسید («Use when editing backend/**/views.py»).

---

## طرح فایل خروجی

```
.opencode/
├── skills/
│   ├── frontend-state-pinia/
│   │   └── SKILL.md
│   └── backend-api-flow/
│       └── SKILL.md
├── agents/
│   ├── architect.md
│   ├── backend.md
│   ├── frontend.md
│   └── reviewer.md
├── instructions/
│   ├── shared-rule-precedence.md
│   └── backend-security-security.md
├── commands/                    # فقط workflowهای دستی انتخابی
│   └── shared-rules-audit-checklist.md
└── opencode.json
AGENTS.md
```

### `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [".opencode/instructions/*.md"],
  "agent": {
    "backend": {
      "mode": "primary"
    }
  },
  "permission": {
    "skill": {
      "*": "allow"
    }
  }
}
```

تعریف کامل ایجنت در markdown کافی است؛ JSON فقط default_agent یا override.

---

## Schema فایل‌ها

### AGENTS.md

```markdown
# Aegis Project Instructions

## Principles
- SSOT, SoC, DRY, KISS, YAGNI. Domain rules win on conflict.

## Policies
- No secrets in git. Python venv required. No CDN in frontend.

## Architecture pointers
- Django services hold business logic. See skill `backend-architecture-django-architecture`.
- Vue atomic design. See skill `frontend-architecture-atomic-design`.

## Agents
Use `@backend`, `@frontend`, `@architect`, `@reviewer` for specialized work.
```

### Instruction (rule/policy)

Markdown ساده. از طریق `instructions` لود می‌شود و با AGENTS.md ترکیب می‌گردد.

### Skill `SKILL.md`

فقط فیلدهای شناخته‌شده:

```yaml
---
name: frontend-state-pinia
description: Pinia store patterns for Vue 3. Use when creating or editing Pinia stores or frontend/src/stores files.
license: MIT
compatibility: opencode
metadata:
  aegis_kind: skill
  aegis_domain: frontend
---

# Pinia

<body>
```

`kind` و `id` را در top-level نگذارید؛ ignore می‌شوند. در `metadata` به‌صورت string.

`description` حداکثر ۱۰۲۴ کاراکتر.

### Agent `.md`

```yaml
---
description: Backend Django/API implementation. Use for REST, models, serializers, and backend tests.
mode: primary
permission:
  edit: allow
  bash: deny
  webfetch: deny
  websearch: deny
---

You are the Backend Engineer Agent. ...
```

Reviewer:

```yaml
---
description: Read-only review for security, standards, and architecture consistency.
mode: all
permission:
  edit: deny
  bash: deny
---
```

### Command (اختیاری برای workflow دستی)

`.opencode/commands/shared-rules-audit-checklist.md` با template پرامپت.

---

## فاصله با emitter فعلی

`emitters/opencode.py` امروز:

- `rule|principle|reference|policy|skill` همه skill می‌شوند → rules پایدار وارد AGENTS.md/`instructions` نمی‌شوند
- `architecture` و `workflow` skip
- ایجنت را JSON در `agents/<id>.json` می‌نویسد؛ docs رسمی markdown در `.opencode/agents/` را ترجیح می‌دهد
- `opencode.json` می‌سازد اما `instructions` ندارد
- `AGENTS.md` نمی‌سازد
- skill frontmatter نسبتاً نزدیک spec است (`name`, `description`, `metadata`) — این بخش قابل حفظ است

هدف: AGENTS.md + instructions برای kind سخت، skills برای اجرایی، agents به‌صورت `.md`.

---

## قواعد کیفیت

1. Frontmatter skill را به پنج فیلد شناخته‌شده محدود کنید.
2. `name` باید دقیقاً نام پوشه باشد و از regex hyphen عبور کند.
3. Rule را فقط skill نکنید؛ OpenCode skill را تا فراخوانی tool لود نمی‌کند.
4. ایجنت را markdown بنویسید؛ `tools` را با `permission` عوض کنید.
5. اگر هم AGENTS.md و هم CLAUDE.md می‌نویسید، OpenCode فقط AGENTS.md را می‌گیرد — محتوا را آنجا بگذارید.
