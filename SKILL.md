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
- Do not auto-save private user writing, private examples, or model outputs as reusable lessons. Public-safe learning must be explicit, metadata-only by default, and reviewed through `prosekernel learn` plus `prosekernel validate-learning`.
- Do not import learning notes directly. Approved safe-rights notes can only generate review-required proposals with `prosekernel propose-example` or `prosekernel propose-pattern`; humans must review before moving anything into `library/` or `patterns/`.
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
9. If learning is explicitly requested, run `prosekernel learn` and then `prosekernel validate-learning`; never store source prose in the learning note. Promotion-ready lessons require `--promote --approved` and safe rights.
10. If a promotion-ready lesson should become corpus work, run `prosekernel propose-example` or `prosekernel propose-pattern`; keep generated files under `proposals/` until human review.

## Useful commands

```bash
python -m pip install -e .
prosekernel --help
prosekernel search-examples "write a launch email for ProseKernel" --mode hybrid --explain
prosekernel brief "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-brief.md
prosekernel write-demo "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-demo.md
prosekernel critique draft.md --task "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-critique.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-rewrite.md --rewrite-output /tmp/prosekernel-rewritten.md
prosekernel learn draft.md --task "write a launch email for ProseKernel" --source-title "Launch draft" --source-author "User" --source-url "https://example.com/launch-draft" --rights user-provided --category email-newsletters --tags "launch, email" --promote --approved --output /tmp/prosekernel-lesson.md
prosekernel validate-learning
prosekernel propose-example /tmp/prosekernel-lesson.md --root /root/prosekernel --output /tmp/prosekernel-example-proposal.md
prosekernel propose-pattern /tmp/prosekernel-lesson.md --root /root/prosekernel --pattern-id PATTERN_EMAIL_999 --output /tmp/prosekernel-pattern-proposal.md
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
