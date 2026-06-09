# Aegis IR Specification v1 — Workflow

## WorkflowIR Node

Represents a workflow template that defines a sequence of agent stages.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"workflow_ir"` |
| `id` | string | Stable identifier, unique across all workflows |
| `name` | string | Human-readable workflow name |
| `description` | string | What this workflow accomplishes |
| `domain` | string | Domain this workflow belongs to |
| `category` | string | Category within the domain |
| `stages` | Stage[] | Ordered sequence of workflow stages |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | string[] | Tags for matching |
| `triggers` | string[] | Regex patterns for auto-matching |
| `agents` | string[] | IDs of agents this workflow uses |
| `capabilities_required` | string[] | IDs of capabilities required |
| `priority` | integer | 0-100 |

### Stage Structure

```yaml
Stage:
  id: string                  # Unique within workflow
  name: string                # Human-readable stage name
  agent: string               # ID of agent to execute this stage
  depends_on: string[]        # IDs of stages this depends on
  required_knowledge: string[] # IDs of knowledge nodes required
  required_capabilities: string[] # IDs of capabilities required
  status: string              # "pending", "active", "completed", "failed"
```

### Relationships

- Workflows reference agents by ID in `stages[].agent`.
- Workflows reference knowledge nodes by ID in `stages[].required_knowledge`.
- Workflows reference capabilities by ID in `stages[].required_capabilities` and `capabilities_required`.
- Agents reference workflows by ID in `workflows`.

### Validation Rules

1. `id` must be unique across all workflow nodes.
2. Stage `id` must be unique within the workflow.
3. All `agent` values in stages must resolve to agent nodes.
4. All `required_knowledge` values must resolve to knowledge nodes.
5. All `required_capabilities` values must resolve to capability nodes.
6. `depends_on` in stages must reference other stages within the same workflow.
7. No circular dependencies in stage graph (DAG validation).
8. All `agents` listed must be referenced in at least one stage.

### What Belongs in Workflow IR

- Workflow templates
- Stage definitions with agent assignments
- Dependency graph between stages
- Trigger patterns for auto-matching
- Capability requirements

### What Does NOT Belong in Workflow IR

- Tool-specific execution parameters
- Runtime scheduling logic
- Emitter-specific formatting
- File output layout
