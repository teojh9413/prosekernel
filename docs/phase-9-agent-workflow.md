# Phase 9 — Agent Workflow Integration

Status: implemented.

ProseKernel is now packaged for coding and writing agents that need an explicit operating loop instead of a vague writing prompt.

Supported targets include Codex, Claude Code, Cursor, OpenCode, Hermes, and any agent that can read Markdown instructions and run CLI commands.

## Core loop

**classify → retrieve → patterns → brief → draft → lint/score → revise → explain**

This loop keeps taste retrieval, pattern transfer, drafting, and quality checks separate enough for an agent to audit its own work.

## Added assets

- `SKILL.md` — repo-local agent skill/instructions.
- `prompts/agent-workflow.md` — end-to-end workflow prompt.
- `prompts/writing-brief.md` — reusable brief contract.
- `prompts/critique.md` — critique prompt for generic AI slop, specificity, proof, reader fit, and non-genericness.
- `prompts/rewrite.md` — rewrite prompt with explicit quality gate.
- `docs/agent-workflow.md` — command-grounded workflow documentation.

## Agent operating model

### 1. Classify

Agents first identify format, reader, goal, awareness stage, required facts, available proof, forbidden claims, and channel constraints.

### 2. Retrieve

```bash
prosekernel search-examples "<task>" --mode hybrid --explain
```

Retrieval should produce examples across same-format, same-goal, and proof/clarity references.

### 3. Build the brief

```bash
prosekernel brief "<task>" --mode hybrid --output /tmp/prosekernel-brief.md
```

The brief is the handoff between retrieval and drafting. It includes examples, pattern IDs, pattern instructions, craft moves, and quality gates. It makes no provider call.

### 4. Draft

The drafting agent writes original prose from the brief. It performs structure transfer, not phrase transfer.

### 5. Lint and score

```bash
prosekernel lint draft.md
prosekernel scorecard draft.md --task "<task>"
```

A failing lint or scorecard is not a cosmetic warning. It means the draft needs another pass.

### 6. Revise and explain

The agent revises for cuts, specificity, proof, structure, and rhythm, then explains what changed and what risks remain.

## Integration notes

### Codex / OpenCode / Claude Code

- Read `SKILL.md` before modifying writing assets.
- Run CLI commands from the repo root.
- Treat prompt/doc changes as tested behavior when covered by `tests/test_agent_workflow_assets.py`.
- Do not add paid provider calls unless explicitly requested.

### Cursor

- Add `SKILL.md` and `docs/agent-workflow.md` to context before writing.
- Use `prompts/writing-brief.md`, `prompts/critique.md`, and `prompts/rewrite.md` as reusable snippets.

### Hermes

- Load the ProseKernel skill before repo work.
- Keep `~/wiki/session-state.md` updated after significant phases.
- Preserve the public-safe rule: do not auto-save private user writing into the reusable corpus.

## Public-safe boundaries

- ProseKernel teaches structure, taste, and craft.
- It is not a private voice clone.
- It is not a copyrighted text mirror.
- Private user drafts are not automatically reusable examples.
- Public-safe learning requires explicit review before a lesson becomes a pattern or library item.

## Verification

Run:

```bash
pytest tests/test_agent_workflow_assets.py -q
pytest
prosekernel --help
prosekernel brief "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-brief.md
prosekernel search-examples "write a launch email for ProseKernel" --mode hybrid --explain
```
