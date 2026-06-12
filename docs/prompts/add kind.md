You are refactoring a structured AI engineering knowledge base.

Goal
Add a new YAML frontmatter field called `kind` to every markdown file inside the `knowledge/` directory.

This knowledge base is tool-agnostic and serves as the source of truth for generating artifacts for AI tools such as Kilo, Cursor, and Agents.

Allowed values for `kind`

- rule
- policy
- principle
- architecture
- workflow
- skill
- reference


Definitions

rule
A strict constraint or rule that must be followed by AI agents or developers. These typically enforce behavior or restrictions.

Examples:
coding rules, security rules, rule precedence, rule authoring standards.


policy
Organizational or engineering policies such as security policies, dependency policies, or infrastructure policies.

Examples:
offline dependency policy, secrets policy, environment policies.


principle
High-level engineering philosophy or design principles that guide decisions but are not strict constraints.

Examples:
engineering principles, meta principles, design philosophy.


architecture
System structure and architectural guidance.

Examples:
system architecture, layering, project structure, architectural patterns.


workflow
A defined development or operational process.

Examples:
git workflow, release process, testing workflow, CI/CD process.


skill
Actionable implementation knowledge that helps an AI agent perform a task.

Examples:
framework usage, implementation patterns, integration patterns, coding techniques.


reference
Quick reference material, summaries, or documentation-style content.

Examples:
cheat sheets, quick references, documentation helpers.


Instructions

1. Scan all files inside:

   knowledge/**/*.md

2. For each file:
   - Read the YAML frontmatter.
   - Preserve all existing fields.
   - Add a new field:

     kind: <classification>

3. Do NOT modify the following fields:

   title  
   summary  
   domain  
   category  
   applies_to  
   priority  

4. Only modify the YAML frontmatter.

5. If a file already contains `kind`, do not duplicate it.

6. Use the file name, summary, and content to determine the most appropriate classification.

7. Be conservative and choose the best semantic match.


Output

Return the modified version of each file with the updated YAML frontmatter including the `kind` field.