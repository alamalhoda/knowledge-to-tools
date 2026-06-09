# Aegis IR Specification v1 — Root

## Overview

The Aegis Intermediate Representation (IR) is the formal architectural contract between the Knowledge Layer, Agent Layer, Runtime Layer, Emitters, and Pipeline Layer.

IR is the **single source of truth** for all downstream consumers.

## IR Version

All IR artifacts include a `version` field identifying the IR schema version.

Current IR version: `2.0`

## IR Root Structure

```yaml
IRRoot:
  version: string                    # IR schema version
  generated_at: string               # ISO 8601 timestamp
  source_hash: string                # SHA256 of source knowledge
  knowledge: KnowledgeGraph          # All knowledge nodes
  capabilities: CapabilityGraph      # Capability declarations
  agents: AgentGraph                 # Agent definitions
  workflows: WorkflowGraph           # Workflow templates
  routes: RouteGraph                 # Routing rules
  contracts: ContractGraph           # Permission/authority contracts
```

## Relationships

- **Agents** reference **Capabilities**, **Knowledge** nodes, and **Workflows** by ID.
- **Workflows** reference **Agents** and **Capabilities** by ID.
- **Routes** reference **Agents** and **Knowledge** nodes by ID.
- **Contracts** reference **Agents** by ID.
- All references must be resolvable within the IR Root.

## Invariants

1. All node IDs are unique across all graphs.
2. All references in agents, workflows, routes, and contracts must resolve to existing nodes.
3. The IR Root is immutable after construction.
4. IR compilation is deterministic: identical inputs produce structurally identical IR.

## Serialization

IR is serialized as JSON with:
- Deterministic key ordering (sorted alphabetically)
- No null values (use empty collections)
- Unicode strings (no escaped sequences where avoidable)
