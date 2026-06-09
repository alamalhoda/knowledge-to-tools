# Aegis IR Specification v1 — Route

## RouteIR Node

Represents a routing decision record that maps a routing context to selected agents and knowledge.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"route_ir"` |
| `id` | string | Unique route identifier |
| `context` | RoutingContext | The input context that triggered this route |
| `selected_agent` | string | ID of the matched agent |
| `selected_knowledge` | string[] | IDs of matched knowledge nodes |
| `confidence` | float | Routing confidence score (0.0-1.0) |

### RoutingContext Structure

```yaml
RoutingContext:
  task: string              # The task description
  domain: string | null     # Detected or provided domain
  intent: string            # Lowercased intent string
  files: string[]           # File paths involved
  metadata: dict            # Additional context
```

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `context_pack` | ContextPack | Expanded context for the selected agent |
| `expanded_knowledge` | string[] | Knowledge nodes after dependency expansion |
| `match_reason` | string | Explanation of routing decision |
| `fallback_used` | boolean | Whether fallback routing was used |

### ContextPack Structure

```yaml
ContextPack:
  task: string
  domain: string | null
  files: string[]
  knowledge_summary: string
```

### Relationships

- Routes reference agents by ID in `selected_agent`.
- Routes reference knowledge nodes by ID in `selected_knowledge` and `expanded_knowledge`.

### Validation Rules

1. `id` must be unique across all route nodes.
2. `selected_agent` must resolve to an agent node.
3. All IDs in `selected_knowledge` must resolve to knowledge nodes.
4. All IDs in `expanded_knowledge` must resolve to knowledge nodes.
5. `confidence` must be in range 0.0-1.0.
6. `context.task` must be a non-empty string.

### What Belongs in Route IR

- Routing context snapshots
- Agent matching results
- Knowledge selection results
- Confidence scores
- Dependency expansion results

### What Does NOT Belong in Route IR

- Routing algorithm implementation
- Scoring weights and heuristics
- Runtime state
- Tool-specific routing configuration
