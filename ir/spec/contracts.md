# Aegis IR Specification v1 — Contracts

## ContractIR Node

Represents permission and authority contracts between agents, capabilities, and operations.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"contract_ir"` |
| `id` | string | Stable identifier, unique across all contracts |
| `name` | string | Human-readable contract name |
| `description` | string | What this contract governs |
| `domain` | string | Domain this contract applies to |
| `parties` | Party[] | Entities bound by this contract |

### Party Structure

```yaml
Party:
  id: string                # Agent or capability ID
  role: string              # "grantor", "grantee", "both"
  permissions: Permissions  # Granted permissions
```

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | string[] | Tags for classification |
| `conditions` | Condition[] | Conditions under which contract applies |
| `expires_at` | string | ISO 8601 expiry timestamp |
| `priority` | integer | 0-100 |
| `metadata` | dict | Additional contract metadata |

### Condition Structure

```yaml
Condition:
  field: string             # Field to check
  operator: string          # "eq", "neq", "in", "not_in", "gt", "lt"
  value: any                # Value to compare against
```

### Relationships

- Contracts reference agents/capabilities by ID in `parties[].id`.

### Validation Rules

1. `id` must be unique across all contract nodes.
2. All `parties[].id` must resolve to agent or capability nodes.
3. `conditions` must be well-formed condition structures.
4. `expires_at` must be a valid ISO 8601 timestamp if present.

### What Belongs in Contract IR

- Permission grants between parties
- Authority delegation contracts
- Conditional access rules
- Contract expiry metadata

### What Does NOT Belong in Contract IR

- Tool-specific permission implementations
- Runtime enforcement logic
- Emitter-specific permission mappings
