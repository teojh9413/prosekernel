# Phase 6 — Provider-Agnostic Brief Mode

Phase 6 starts with `brief` before any paid/API-backed `write` command.

The goal is to make ProseKernel useful to any agent without assuming credentials. A brief is a complete drafting packet: retrieved examples, strict pattern IDs, pattern instructions, craft moves, an agent-ready prompt, and a quality gate.

## Command

```bash
prosekernel brief "write a launch email for ProseKernel" --output /tmp/prosekernel-brief.md
```

Equivalent module form while developing:

```bash
PYTHONPATH=src python3 -m prosekernel.cli brief "write a launch email for ProseKernel" --output /tmp/prosekernel-brief.md
```

## What the brief includes

- recommended categories
- retrieved examples
- pattern IDs attached to those examples
- strict pattern agent instructions from `patterns/PATTERN_*.md`
- craft moves extracted from annotations
- a provider-neutral drafting prompt
- quality gate commands:
  - `prosekernel lint draft.md`
  - `prosekernel scorecard draft.md --task "..."`

## Safety / cost rule

`prosekernel brief` never calls a model and never reads API keys. It is dry-run mode by design.

This protects users from accidental API spend and gives agent platforms a stable input packet they can pass to their own model of choice.

## Provider adapter status

Phase 6A brief mode is stable. Phase 6B has since added explicit provider-backed `write` mode; see `docs/phase-6b-provider-write.md`.

Current provider adapter flow:

```text
task → retrieve examples/patterns → build brief → explicit provider drafts → lint → scorecard → report
```

Provider adapters are explicit and credential-safe:

- `--provider openai|anthropic|openrouter`
- `--model MODEL_NAME`
- `brief` remains available without credentials or model calls
- no default paid provider
- clear error if required environment variables are missing

The brief contract must stay stable so Codex, Claude Code, Cursor, OpenCode, Hermes, or any other agent can consume it without depending on a specific LLM vendor.
