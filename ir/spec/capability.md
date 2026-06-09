# Aegis IR Specification v1 — Capability

## CapabilityIR Node

Represents a named capability that agents can declare and workflows can require.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"capability_ir"` |
| `id` | string | Stable identifier, unique across all capabilities |
| `name` | string | Human-readable name |
| `description` | string | What this capability enables |
| `domain` | string | Domain this capability belongs to |
| `category` | string | Category within the domain |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | string[] | Tags for matching |
| `requires` | string[] | IDs of other capabilities this depends on |
| `provides` | string[] | IDs of capabilities this satisfies |
| `priority` | integer | 0-100 |

### Relationships

- Capabilities can `require` other capabilities.
- Agents declare capabilities they possess.
- Workflows declare capabilities they require.

### Validation Rules

1. `id` must be unique across all capability nodes.
2. All IDs in `requires` and `provides` must resolve to existing capability nodes.
3. No circular dependency chains in `requires` graph.

### What Belongs in Capability IR

- Capability declarations
- Dependency chains between capabilities
- Domain and category classification

### What Does NOT Belong in Capability IR

- Tool-specific capability mappings
- Implementation details
- Runtime execution logic
