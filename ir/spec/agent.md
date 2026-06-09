# Aegis IR Specification v1 — Agent

## AgentIR Node

Represents an agent definition composed from knowledge and configuration.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"agent_ir"` |
| `id` | string | Stable identifier, must match agent config key |
| `name` | string | Machine name |
| `display_name` | string | Human-readable display name |
| `description` | string | Agent purpose and role |
| `role` | string | Agent role classification |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `domains` | string[] | Knowledge domains this agent operates in |
| `skills` | string[] | IDs of knowledge nodes bound as skills |
| `workflows` | string[] | IDs of workflow templates this agent participates in |
| `blueprints` | string[] | IDs of architecture blueprints this agent follows |
| `bundles` | string[] | IDs of bundle references |
| `capabilities` | string[] | IDs of capability nodes this agent possesses |
| `permissions` | Permissions | Permission model |
| `behavior` | Behavior | Behavioral configuration |
| `authority` | Authority | Authority level configuration |
| `routing` | Routing | Routing priority and matching rules |

### Permissions Structure

```yaml
Permissions:
  shell: boolean           # Allow shell execution
  edit: boolean            # Allow file editing
  read: boolean            # Allow file reading (default: true)
  network: boolean         # Allow network access
  planning: string         # "required", "preferred", "optional"
  review: string           # "required", "preferred", "optional"
  testing: string          # "required", "preferred", "optional"
```

### Behavior Structure

```yaml
Behavior:
  planning: string         # "required", "preferred", "optional"
  testing: string          # "required", "preferred", "optional"
  review_style: string     # "strict", "balanced", "lenient"
  response_format: string  # "detailed", "concise", "minimal"
```

### Authority Structure

```yaml
Authority:
  level: string            # "junior", "mid", "senior", "lead", "architect"
  can_delegate: boolean
  escalation_path: string[] # IDs of agents to escalate to
```

### Routing Structure

```yaml
Routing:
  priority: integer        # Routing priority weight
  match_domains: string[]  # Domains this agent matches
  match_patterns: string[] # File patterns for matching
```

### Relationships

- Agents reference knowledge nodes via `skills`, `workflows`, `blueprints`.
- Agents reference capabilities via `capabilities`.
- Agents reference other agents via `authority.escalation_path`.
- Contracts reference agents by ID.

### Validation Rules

1. `id` must be unique across all agent nodes.
2. All IDs in `skills` must resolve to knowledge nodes.
3. All IDs in `workflows` must resolve to workflow nodes.
4. All IDs in `blueprints` must resolve to knowledge nodes with `kind == "architecture"`.
5. All IDs in `capabilities` must resolve to capability nodes.
6. All IDs in `authority.escalation_path` must resolve to agent nodes.
7. `permissions`, `behavior`, `authority` must be valid dictionaries.

### What Belongs in Agent IR

- Agent profile and metadata
- Knowledge bindings (skills, workflows, blueprints)
- Capability declarations
- Permission model
- Behavior configuration
- Authority configuration
- Routing configuration

### What Does NOT Belong in Agent IR

- Tool-specific configuration (model names, temperature, etc.)
- CLI parameters
- Emitter-specific formatting
- File output layout
- Runtime orchestration logic
