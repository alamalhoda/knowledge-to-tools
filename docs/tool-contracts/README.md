# قرارداد خروجی ابزارها / Tool Output Contracts

این پوشه مشخص می‌کند هر ابزار AI **چه artifact بومی** دارد و هر `kind` دانش Aegis باید به کدام artifact تبدیل شود.

منبع دانش: `knowledge/` با هفت kind (`rule`, `policy`, `principle`, `architecture`, `workflow`, `skill`, `reference`) به‌علاوه موجودیت جدا `agents`.

تاریخ بررسی مستندات رسمی: **۱۲ اوت ۲۰۲۶**.

| ابزار | سند قرارداد | Emitter فعلی |
|---|---|---|
| [Cursor](https://cursor.com/docs) | [cursor.md](cursor.md) | `emitters/cursor.py` |
| [Kilo](https://kilo.ai/docs) | [kilo.md](kilo.md) | `emitters/kilo.py` |
| [Claude Code](https://code.claude.com/docs) | [claude.md](claude.md) | `emitters/claude.py` |
| [OpenCode](https://opencode.ai/docs) | [opencode.md](opencode.md) | `emitters/opencode.py` |

## نگاشت خلاصه

| Kind Aegis | Cursor | Kilo | Claude Code | OpenCode |
|---|---|---|---|---|
| `rule` | `.cursor/rules/*.mdc` | `.kilo/rules/*.md` + `instructions` | `.claude/rules/*.md` | `AGENTS.md` یا `instructions` |
| `policy` | `.mdc` با `alwaysApply` یا glob | `.kilo/rules/*.md` | `.claude/rules/*.md` یا `CLAUDE.md` | `AGENTS.md` |
| `principle` | `.mdc` با `alwaysApply` برای اولویت بالا | `AGENTS.md` / rules | `CLAUDE.md` (کوتاه) | `AGENTS.md` |
| `architecture` | skill با `paths` یا بخش AGENTS.md | skill یا instructions | `CLAUDE.md` کوتاه + skill جزئیات | `AGENTS.md` کوتاه + skill |
| `workflow` | skill (روی تقاضا) | skill | skill (`/name`) | skill یا `commands/` |
| `skill` | `.cursor/skills/<id>/SKILL.md` | `.kilo/skills/<id>/SKILL.md` | `.claude/skills/<id>/SKILL.md` | `.opencode/skills/<id>/SKILL.md` |
| `reference` | skill + `references/` | skill + `references/` | skill (on-demand) | skill |
| `agents` | `.cursor/agents/<id>.md` | `.kilo/agents/<id>.md` | `.claude/agents/<id>.md` | `.opencode/agents/<id>.md` |

استاندارد مشترک مهارت‌ها: [Agent Skills](https://agentskills.io) — پوشه با `SKILL.md`، frontmatter `name` + `description`.

## اصل طراحی emitter

1. IR ابزار-آگنوستیک می‌ماند؛ فقط emitter فرمت بومی می‌نویسد.
2. kind سخت (`rule` / `policy`) باید **همیشه یا با glob** در context باشد، نه فقط skill روی تقاضا.
3. kind اجرایی (`skill` / `workflow` / `reference`) باید **روی تقاضا** بار شود تا context هدر نرود.
4. `architecture` و `principle` خلاصهٔ همیشه-روشن دارند؛ جزئیات در skill.
5. `agents` نقش جدا هستند (context ایزوله + مجوز)، نه فایل دانش.
