# AI-Assisted Feature Implementation Guide

> A systematic, repeatable process for Django/Python engineers to use AI 
> effectively across the full feature development lifecycle.

---

## How to Use This Guide

This process is split into **two chats** — one for thinking, one for building.
Each chat has clear inputs and outputs. Never skip the handoff step.

```
CHAT 1 — THINK                        CHAT 2 — BUILD
───────────────────────────────────   ───────────────────────────────────
Step 1:  Requirement Clarification    Step 4:  Implementation
Step 2:  Feature Specification        Step 5:  Self-Review
Step 3:  Technical Design             Step 6:  Test Generation
                                      Step 7:  Integration Check

OUTPUT: Two .md files                 INPUT:  Those two .md files
  - feature_spec.md                           + codebase context
  - implementation_plan.md
```

---

## File Structure

Store all generated documents in version control alongside your code:

```
your-django-project/
└── ai-documents/
    └── features/
        └── <feature-name>/
            ├── feature_spec.md
            ├── implementation_plan.md
            └── integration_check.md
```

**Naming convention:** Use the Django app name or main model the feature touches.
Examples: `user-authentication`, `payment-processing`, `llm-summary-service`

**Commit these files.** They are the living documentation of why your code works
the way it does. If a feature is significantly changed later, either update the
spec or create a new folder: `user-authentication-v2`.

---

## Service Types

Your features fall into three types. You will declare the type in each prompt —
it changes what questions get asked and what rules apply.

| Type | Description |
|---|---|
| 🗄️ DB-BACKED SERVICE | Django models, ORM, migrations, transactions |
| 🧠 INTELLIGENT SERVICE | LLM integrations, prompt chains, pipelines |
| 🌐 AUTOMATION SERVICE | Selenium, browser automation, web interactions |

---

## CHAT 1 — THINK

---

### Step 1: Requirement Clarification

**Purpose:** Surface ambiguities and edge cases before any design or code is written.

**Input:** Your user story + service type
**Output:** A numbered list of clarifying questions — answer all of them before Step 2

```
You are a senior software engineer doing a requirement review before implementation.

## Service Type
[DB-BACKED SERVICE | INTELLIGENT SERVICE | AUTOMATION SERVICE]

## User Story
[PASTE USER STORY HERE]

## Additional Context
[Any extra notes, constraints, or background]

---

Your job is NOT to write code yet.

Based on the service type and user story above, ask me the most important
clarifying questions a senior engineer would ask before starting implementation.

Focus your questions on:

If DB-BACKED SERVICE:
- Data model ambiguities (relationships, nullable fields, uniqueness)
- Business rule edge cases
- Read/write performance expectations
- What happens on failure or partial completion

If INTELLIGENT SERVICE:
- What is the exact input and expected output format
- Which LLM / model is being used, or is it flexible
- How should hallucinations or low-confidence outputs be handled
- Latency and cost sensitivity
- Does the output feed into another system

If AUTOMATION SERVICE:
- What triggers this automation (scheduled, on-demand, event-driven)
- How to handle failures mid-flow (partial completion, retries)
- Are there login/auth steps involved
- What does success/failure look like and how is it reported
- Are there rate limiting or anti-bot concerns

For ALL service types also ask about:
- Who are the consumers of this service (internal, external, other devs)
- Are there existing similar patterns in the codebase to follow
- What is out of scope for this feature

Return a numbered list of questions only. No code, no suggestions yet.
```

**After this step:** Answer every question in the chat before proceeding to Step 2.

---

### Step 2: Feature Specification

**Purpose:** Formally capture what the feature must do in precise, testable language.
Written now — while requirements are freshest — so that the technical design in
Step 3 is driven by the spec, not the other way around.

**Input:** Answered questions from Step 1 (already in chat context)
**Output:** `feature_spec.md`

```
Based on our requirements discussion, generate a feature specification
file called `feature_spec.md`.

This file has two jobs:
1. It drives the technical design in the next step
2. It will be used in Chat 2 to generate tests

So it must capture behavior precisely — not architecture, not code,
just what the feature does and how it should behave in every scenario.

---

## File Structure

### 1. Feature Overview
- One paragraph summary of what this feature does and why it exists
- The service type (DB-backed / Intelligent / Automation)
- Primary consumers of this feature (who or what calls it)

### 2. Inputs & Outputs
- Every input this feature accepts: name, type, required/optional, constraints
- Every output this feature returns: shape, type, and what each field means
- If it's an API endpoint, include the request/response contract

### 3. Business Rules
A numbered list of explicit rules the feature must enforce.
Each rule should be a single, testable statement. Examples:
- "A user cannot submit a request if their account is inactive"
- "If the LLM returns malformed JSON, the service must retry up to 3 times"
- "A task must not be marked complete if any of its subtasks are still pending"

### 4. Acceptance Scenarios
Written in plain language, not code. For each scenario use this format:

**Scenario [N]: [Short name]**
- Given: [initial state or context]
- When: [the action or input]
- Then: [the expected outcome]

Cover these scenario types:
- Happy path (the normal successful flow)
- Edge cases (boundary values, empty inputs, minimum/maximum)
- Failure cases (what happens when things go wrong)
- For intelligent services: unexpected or malformed LLM output
- For automation services: mid-flow failures, element not found, timeouts

### 5. Out of Scope
Explicitly list what this feature does NOT handle.
This prevents scope creep in both implementation and tests.

---

## Rules for Writing This Spec
- Every statement must be testable — if you can't write a test for it, rewrite it
- No implementation details — say WHAT, never HOW
- No ambiguous language — avoid "should handle gracefully",
  instead say exactly what happens
- If something is still ambiguous, flag it with: ⚠️ OPEN QUESTION: [question]
  rather than making an assumption silently
```

**After this step:** Read `feature_spec.md` carefully and resolve any
`⚠️ OPEN QUESTION` items before moving to Step 3.

---

### Step 3: Technical Design

**Purpose:** Decide how to build what the spec describes. The design is explicitly
driven by `feature_spec.md` — not the other way around.

**Input:** `feature_spec.md` (already in chat context)
**Output:** `implementation_plan.md`

```
Using feature_spec.md as the source of truth, produce a technical design
for this feature and write it to a file called `implementation_plan.md`.

Do NOT write implementation code yet.

---

## Phase 1 — Design Brief
First, present the design for my review with these sections:

### 1. Service Architecture
- What functions/classes/modules need to be created or modified
- How they relate to each other (call flow)
- Where this fits in the existing project structure

### 2. Data Layer (skip if not applicable)
- New or modified Django models
- Key fields, relationships, and constraints to be aware of
- Whether any migrations have non-trivial risk

### 3. External Dependencies
- Any new libraries, APIs, or services needed
- LLM model/tools if this is an intelligent service
- Browser/driver considerations if this is an automation service

### 4. Error Handling Strategy
- What can go wrong at each major step
- How failures should be surfaced (exception, return value, logging)

### 5. Open Questions / Risks
- Anything still ambiguous after reviewing feature_spec.md
- Technical risks or tradeoffs worth flagging before coding starts

Keep each section concise — this is a design brief, not documentation.
Flag anything where you see multiple valid approaches and briefly state
the tradeoff.

Wait for my approval before proceeding to Phase 2.

---

## Phase 2 — Write the Plan
Once I approve the design, write `implementation_plan.md`:

# Implementation Plan — [Feature Name]

## Architecture Summary
[One paragraph summary of the agreed approach]

## Implementation Steps
- [ ] Step 1: [e.g. Create/modify models]
- [ ] Step 2: [e.g. Write service logic]
- [ ] Step 3: [e.g. Write utilities]
- [ ] Step 4: [e.g. Wire up views/entry point]

## Key Decisions & Assumptions
[Any tradeoffs or assumptions made during design that Chat 2 should know about]

## Open Questions
[Any unresolved ⚠️ items from feature_spec.md that must be addressed
before or during implementation]
```

**After this step:** Chat 1 is complete. You now have two files ready to hand
off: `feature_spec.md` and `implementation_plan.md`. Commit both to
`ai-documents/features/<feature-name>/` before opening Chat 2.

---

## CHAT 2 — BUILD

### Handoff Prompt (Always Start Chat 2 With This)

**Purpose:** Load context into a fresh chat cleanly, without relying on
conversation history.

```
I am implementing a new feature. The thinking and design phase is complete.
Here are the reference files you must read before we start:

- feature_spec.md — the full requirements and acceptance scenarios
- implementation_plan.md — the agreed technical design

Rules:
- Treat these files as the source of truth, not our conversation
- If anything in the codebase contradicts the spec, flag it, don't silently decide
- We will follow the step-by-step implementation loop from implementation_plan.md

Start by reading both files and confirming you understand the feature
and the plan. Then wait for me to say "begin".
```

---

### Step 4: Implementation

**Purpose:** Build the feature in controlled, reviewable steps.

**Input:** `feature_spec.md` + `implementation_plan.md` + codebase context
**Output:** Working code + `implementation_plan.md` updated with checkboxes

```
Now implement the feature following implementation_plan.md exactly.

## Execution Rules
- Implement only one step at a time
- After completing each step, mark it done in implementation_plan.md:
  `- [x] Step description`
- Add a short note under the step if you made any assumptions
- Wait for my review and confirmation before moving to the next step
- Repeat until all steps are complete

---

## Implementation Rules

### General
- Follow the existing code style and patterns you see in this project
- Use type hints on all functions and methods
- Every function must have a docstring (one line is fine for simple functions)
- No magic numbers or hardcoded strings — use constants or config
- Keep functions small and single-purpose

### Error Handling
- Never silently swallow exceptions
- Use specific exception types, not bare `except:`
- Log errors with enough context to debug (include relevant IDs, inputs)
- Raise custom exceptions where the caller needs to handle failure explicitly

### Django-Specific (skip if not applicable)
- Use select_related / prefetch_related where you touch related objects
- Any multi-step DB writes must be wrapped in a transaction
- Never put business logic in views — it belongs in services or managers
- Serializer validation should be strict, not lenient

### Intelligent Service-Specific (skip if not applicable)
- Separate prompt templates from business logic
- LLM calls must have error handling for timeouts and malformed responses
- Log the raw LLM input/output at DEBUG level for traceability
- Never trust LLM output without validation against expected format

### Automation Service-Specific (skip if not applicable)
- Each major browser action should be wrapped in a try/except
- Add explicit waits, never implicit/hardcoded sleep where avoidable
- Log each major step so failures are easy to locate in logs
- Make the automation resumable or at minimum clearly report where it failed

---

## Output Format Per Step
For each step, produce code and end with:
# ---- REVIEW NOTE ----
# What this step did, assumptions made, and anything I should double-check
# Next step will be: [brief description of next step]
```

---

### Step 5: Self-Review

**Purpose:** Catch errors, gaps, and inconsistencies before tests are written.

**Input:** Completed implementation + `feature_spec.md` (in chat context)
**Output:** Inline fixes + final `implementation_plan.md` update

```
Review the code you just implemented against the checklist below.
Do NOT rewrite everything — only flag and fix real issues you find.

For each section, explicitly state:
- ✅ PASS — if everything looks good, briefly say why
- ⚠️ ISSUE — if something needs fixing, explain what and fix it immediately
- N/A — if the section doesn't apply to this service type

---

## Review Checklist

### 1. Correctness
- Does the implementation match every business rule in feature_spec.md?
- Are all acceptance scenarios from feature_spec.md actually handled?
- Are there any ⚠️ OPEN QUESTIONS in the spec that were never resolved?

### 2. Error Handling
- Is every external call wrapped in proper error handling?
  (DB queries, LLM calls, HTTP requests, browser actions)
- Are exceptions specific, never bare `except:`
- Are errors logged with enough context to debug in production?
- Does the caller receive a meaningful signal when something fails?

### 3. Edge Cases
- What happens with empty inputs or None values?
- What happens at boundary values (empty list, single item, max size)?
- Are there any assumptions in the code that could silently fail?

### 4. Django-Specific (skip if not applicable)
- Are multi-step DB writes wrapped in transactions?
- Are there any N+1 query risks?
- Is business logic leaking into views or serializers?
- Are there any missing indexes on fields used in filters or lookups?

### 5. Intelligent Service-Specific (skip if not applicable)
- Is LLM output validated before being used downstream?
- Is the retry logic actually tested against malformed responses?
- Are prompt templates decoupled from business logic?
- Is token usage being logged or tracked?

### 6. Automation Service-Specific (skip if not applicable)
- Is every browser interaction protected against timeout/not-found?
- Are there any hardcoded sleeps that should be explicit waits?
- Is the failure point clearly logged if the automation breaks mid-flow?
- Is there any cleanup needed if the automation fails halfway?

### 7. Code Quality
- Are there any functions doing more than one thing?
- Are there any hardcoded strings or magic numbers that should be constants?
- Are all functions typed and have docstrings?
- Is there any dead code or commented-out blocks left behind?

### 8. Security (flag only, don't over-engineer)
- Is any sensitive data being logged that shouldn't be?
- Is user input being trusted anywhere without validation?
- Are any credentials or secrets hardcoded?

---

## After the Review
- Update implementation_plan.md with a final entry:
  `- [x] Self-review complete — [N] issues found and fixed`
- If any ⚠️ OPEN QUESTIONS remain unresolved from feature_spec.md,
  list them explicitly so I can make a decision before tests are written
```

---

### Step 6: Test Generation

**Purpose:** Write a test suite anchored to intended behavior, not inferred from code.

**Input:** `feature_spec.md` + reviewed implementation (in chat context)
**Output:** Test files + `conftest.py` additions

```
Using feature_spec.md as the source of truth, generate a comprehensive
test suite for the feature we just implemented and reviewed.

Do NOT infer test cases from the code — derive them from feature_spec.md.
The code tells you how it works, the spec tells you how it SHOULD work.

---

## Naming Convention

### Default Pattern (logic, business rules, edge cases)
test_<subject>__when_<context>__then_<expected_behavior>()

### HTTP Pattern (endpoint/integration tests)
test_<httpverb>_<endpoint>__when_<context>__then_<expected_behavior>()

### Rules
- Always snake_case, always descriptive, never abbreviated
- No numeric status codes in names UNLESS the status itself is the focus
  Valid exception: test_post_verify__when_rate_limited__then_429_too_many_requests()
- One behavior per test, no vague names like test_verify_success()
- Use pytest.mark.parametrize with ids= for variations of the same scenario:
  @pytest.mark.parametrize("identifier", ["email", "phone"], ids=["email","phone"])
- Helper functions that are not tests must be prefixed with _

---

## Test Structure

### 1. Unit Tests
- One test per business rule listed in feature_spec.md
- Mock all external dependencies (DB, LLM calls, HTTP, browser)
- Test each rule in isolation — no chaining of behaviors in one test

### 2. Edge Case Tests
- Cover every edge case listed in feature_spec.md
- Also cover: None inputs, empty strings, empty lists, boundary values
- For intelligent services: malformed LLM response, timeout, empty response
- For automation services: element not found, timeout, mid-flow failure

### 3. Failure Case Tests
- Every failure scenario from feature_spec.md must have a test
- Assert on the specific exception type raised, not just that it failed
- Assert on log output where logging is part of the contract

### 4. Integration / Endpoint Tests (skip if no API layer)
- Use HTTP pattern naming
- Test the full request → response cycle
- Use pytest fixtures for auth, client setup, and test data
- Assert on response shape, not just status code

---

## Test File Organization
- Group tests in classes by subject:
  class TestVerify:
      def test_verify__when_...
      def test_verify__when_...

  class TestSend:
      def test_send__when_...

- One test file per feature module, named: test_<module_name>.py
- Shared fixtures go in conftest.py, not inside test files

---

## Output Format
Produce tests in this order:
1. conftest.py additions (fixtures needed for this feature)
2. Unit tests
3. Edge case tests
4. Failure case tests
5. Integration tests (if applicable)

After all tests are written, produce a short coverage summary:
# ---- COVERAGE SUMMARY ----
# Business rules covered: X/X from feature_spec.md
# Acceptance scenarios covered: X/X from feature_spec.md
# Open questions that could not be tested: [list any ⚠️ items]
```

---

### Step 7: Integration Check

**Purpose:** Zoom out and assess the impact of this feature on the rest of the system.

**Input:** All code produced in Chat 2 + codebase context
**Output:** `integration_check.md`

```
Now that the feature is implemented and tested, perform an integration check.
Do NOT write new code yet — this is an analysis step.

Review the newly implemented code in the context of the entire codebase
and produce an integration report saved to `integration_check.md`.

---

## Integration Check Sections

### 1. Breaking Changes
- Does this feature change any existing function signatures or return types?
- Does it modify any shared models, serializers, or utilities?
- Does it change any existing API contracts (request/response shape)?
- Are there any other parts of the codebase that call modified code
  and may now behave differently?

For each breaking change found:
⚠️ BREAKING: [what changed] → [what is affected] → [recommended fix]

### 2. Database Impact (skip if not applicable)
- Are there any new migrations that could be risky on a live database?
  (adding non-nullable columns, dropping columns, renaming fields)
- Are there any queries in the new code that could cause performance
  issues at scale? (missing indexes, full table scans, N+1 risks)
- Are there any data integrity risks if the migration runs mid-traffic?

For each issue found:
⚠️ DB RISK: [what the risk is] → [recommended mitigation]

### 3. LLM Integration Impact (skip if not applicable)
- Does this feature introduce new LLM calls that affect latency
  of any existing flows?
- Are there shared prompt templates or LLM clients being modified?
- Could the new LLM behavior affect any existing features that
  depend on the same model or pipeline?

### 4. Automation Impact (skip if not applicable)
- Does this automation share any browser sessions or drivers
  with existing automations?
- Could scheduling or timing of this automation conflict with
  existing ones?
- Are there shared selectors or page interaction patterns
  that could be affected by changes here?

### 5. Configuration & Environment
- Are there new environment variables or settings required?
- Are they documented and do they have safe defaults?
- Will this feature behave differently across dev/staging/production
  environments in any unexpected way?

### 6. Dependency Impact
- Are any new libraries being introduced?
- Do they conflict with existing dependencies in requirements.txt?
- Are there any licensing or security concerns with new packages?

### 7. Backwards Compatibility
- If this feature is behind an API, is the old contract still honored?
- If existing data is affected, is there a migration or backfill needed?
- Are there any consumers of this feature (internal or external) that
  need to be notified of changes?

---

## Output Format

Produce integration_check.md with:
- One section per category above
- ✅ CLEAR — if no issues found in that section
- ⚠️ RISK — for each issue found, with recommended action
- N/A — if the section doesn't apply

End the file with a final summary:

## Integration Verdict
- 🟢 READY — no issues found, safe to merge
- 🟡 MERGE WITH CAUTION — issues found but have clear mitigations
- 🔴 NEEDS WORK — blocking issues that must be resolved before merging

List any action items that must be completed before this feature
is considered done.
```

---

## Quick Reference Cheatsheet

```
CHAT 1 — THINK
──────────────────────────────────────────────────────────────────
Step 1   Requirement Clarification   → Q&A answered in chat
Step 2   Feature Specification       → feature_spec.md ✅
Step 3   Technical Design            → implementation_plan.md ✅

         Commit both files to ai-documents/features/<feature-name>/
         before opening Chat 2.

HANDOFF
──────────────────────────────────────────────────────────────────
         Load feature_spec.md + implementation_plan.md into a
         fresh chat. AI confirms understanding. You say "begin".

CHAT 2 — BUILD
──────────────────────────────────────────────────────────────────
Step 4   Implementation              → code + updated plan ✅
Step 5   Self-Review                 → fixes + final plan ✅
Step 6   Test Generation             → test_*.py + conftest.py ✅
Step 7   Integration Check           → integration_check.md ✅

COMMIT
──────────────────────────────────────────────────────────────────
         ai-documents/features/<feature-name>/
           ├── feature_spec.md
           ├── implementation_plan.md
           └── integration_check.md
```

---

> **Guiding principle:**
> The prompts are only as good as your discipline to follow the process under
> deadline pressure. The `ai-documents/` files are your safeguard —
> if they exist and are complete, you did the process right.
