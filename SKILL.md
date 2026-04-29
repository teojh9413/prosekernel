---
name: prosekernel
description: "Use ProseKernel as an open-source taste engine for AI writing agents."
version: 1.0.0
author: ProseKernel maintainers
license: MIT
metadata:
  tags: [writing, agents, taste, anti-slop, retrieval, evals]
---

# ProseKernel Agent Skill

ProseKernel is an open-source taste engine for AI writing agents.

Use this skill when an agent needs to write, critique, rewrite, or evaluate prose with ProseKernel's public-safe library, pattern layer, and eval tools.

## Operating contract

- Do structure transfer, not phrase transfer.
- Do not copy source phrases.
- Do not mirror copyrighted writing.
- Use source metadata, short excerpts only when legally appropriate, and original craft analysis.
- Do not auto-save private user writing, private examples, or model outputs as reusable lessons. Public-safe learning must be explicit and reviewed.
- Do not choose a paid LLM provider implicitly. `prosekernel write` requires explicit `--provider` and `--model`.

## Default workflow

Follow this loop for serious writing:

1. Classify the job: format, reader, goal, awareness stage, constraints.
2. Retrieve examples with `prosekernel search-examples "<task>" --mode hybrid --explain`.
3. Build an agent-ready packet with `prosekernel brief "<task>" --mode hybrid --output /tmp/prosekernel-brief.md`.
4. Draft from the brief using structure transfer, not phrase transfer.
5. Run `prosekernel lint draft.md`.
6. Run `prosekernel scorecard draft.md --task "<task>"`.
7. Revise until the draft has specific proof, reader fit, and non-genericness.
8. Explain what changed: structure, proof, cuts, specificity, voice, and remaining trade-offs.

## Useful commands

```bash
python -m pip install -e .
prosekernel --help
prosekernel search-examples "write a launch email for ProseKernel" --mode hybrid --explain
prosekernel brief "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-brief.md
prosekernel write-demo "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-demo.md
prosekernel lint draft.md
prosekernel scorecard draft.md --task "write a launch email for ProseKernel"
prosekernel validate-library
prosekernel eval
```

## Prompt assets

- `prompts/agent-workflow.md` — end-to-end agent operating loop.
- `prompts/writing-brief.md` — reusable brief contract.
- `prompts/critique.md` — critique contract for generic AI slop, proof, specificity, reader fit, and non-genericness.
- `prompts/rewrite.md` — rewrite contract with final quality gate.
- `docs/phase-9-agent-workflow.md` — integration notes for Codex, Claude Code, Cursor, OpenCode, Hermes, and other coding/writing agents.

## Quality bar

A ProseKernel draft is not ready until it passes:

- source-safe structure transfer,
- concrete proof before praise,
- no banned slop phrases,
- visible reader fit,
- scorecard review,
- a short explanation of what changed during revision.
