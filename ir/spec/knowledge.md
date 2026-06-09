# Aegis IR Specification v1 — Knowledge

## KnowledgeIR Node

Represents a single knowledge document from the Knowledge Layer.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"knowledge_ir"` |
| `id` | string | Stable slugified identifier, unique across all knowledge |
| `source` | string | Relative path to source file (e.g., `knowledge/backend/api/rest.md`) |
| `domain` | string | Domain: `shared`, `backend`, `frontend`, `devops`, `security`, `data` |
| `category` | string | Category: `architecture`, `rule`, `policy`, `principle`, `workflow`, `skill`, `reference`, `configuration`, `database`, `documentation`, `logging`, `patterns`, `performance`, `testing`, `security`, `api` |
| `kind` | string | Granular kind: `rule`, `policy`, `principle`, `architecture`, `workflow`, `skill`, `reference` |
| `content` | Content | Structured content extracted from source |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | string[] | Freeform tags for matching |
| `priority` | integer | 0-100, higher = more important |
| `status` | string | `draft`, `active`, `deprecated` |
| `applies_to` | string[] | File glob patterns for activation |
| `depends_on` | string[] | IDs of knowledge nodes this depends on |
| `related` | string[] | IDs of related knowledge nodes |
| `checksum` | string | SHA256 of source content |

### Content Structure

```yaml
Content:
  raw: string            # Full source text (truncated if > 8000 chars)
  summary: string        # One-line summary
  key_points: string[]   # Extracted key points (max 20)
  sections: string[]     # Extracted headings
  code_blocks: string[]  # Extracted code examples (max 10)
```

### Activation

```yaml
Activation:
  file_patterns: string[]  # Glob patterns for file matching
  keywords: string[]       # Extracted keywords for intent matching
```

### Relationships

- `depends_on`: Direct dependencies on other knowledge nodes.
- `related`: Soft associations to other knowledge nodes.

### Validation Rules

1. `id` must be unique across all knowledge nodes.
2. `domain` must be one of the allowed domains.
3. `kind` must be one of the allowed kinds.
4. `priority` must be in range 0-100.
5. `status` must be one of `draft`, `active`, `deprecated`.
6. `source` must be a relative path string.
7. `content.raw` must be a non-empty string.
8. All IDs in `depends_on` and `related` must resolve to existing knowledge nodes.

### What Belongs in Knowledge IR

- Extracted content from markdown knowledge files
- Activation metadata (file patterns, keywords)
- Dependency and relationship graphs
- Priority and status metadata

### What Does NOT Belong in Knowledge IR

- Tool configuration
- CLI parameters
- Emitter-specific formatting
- File output layout
- Runtime orchestration logic
