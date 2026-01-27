# AGENTS.md

This file guides coding agents working in this repository.

## Basics
- Keep changes small and explain intent in plain language.
- Prefer existing patterns and conventions in the codebase.
- Ask before making destructive or broad changes.

## Scope
- Safe to edit: source files, tests, docs, and scripts under this repo.
- Do not edit: user data, external repos, or unknown generated files.

## Workflow
- Read the relevant files before editing.
- Use ripgrep (`rg`) for fast searches.
- Keep edits focused to the task; avoid drive-by refactors.

## Tests
- Run the smallest relevant test(s) when feasible.
- If tests are not run, say so and why.

## Output
- Summarize what changed and where.
- Provide next-step suggestions only when useful.
