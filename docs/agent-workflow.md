# Agent Workflow

Use this whenever an AI agent writes with ProseKernel.

The Phase 9 loop is:

**classify → retrieve → patterns → brief → draft → lint/score → revise → explain**

For copy-paste prompt contracts, see:

- `prompts/agent-workflow.md`
- `prompts/writing-brief.md`
- `prompts/critique.md`
- `prompts/rewrite.md`

For integration notes across Codex, Claude Code, Cursor, OpenCode, Hermes, and other agents, see `docs/phase-9-agent-workflow.md`. For productized critique/rewrite reports and short CLI aliases, see `docs/phase-10-productized-cli.md`. For explicit metadata-only learning notes, see `docs/phase-11-public-safe-learning-loop.md`.

## Step 1: Classify the job

Identify:

- Format: tweet, thread, essay, landing page, memo, email, doc, speech, product microcopy, incident note.
- Reader: one specific person, role, or persona.
- Goal: what should change after reading?
- Awareness stage: unaware, problem-aware, solution-aware, product-aware, most-aware.
- Constraints: length, channel, required facts, forbidden claims, tone, legal/compliance boundaries.

## Step 2: Retrieve examples

Use the CLI instead of manually browsing when possible:

```bash
prosekernel search-examples "<task>" --mode hybrid --explain
```

Pick 3-5 examples matching the job.

At minimum:

- one same-format example,
- one same-goal example,
- one proof or clarity reference,
- one anti-slop or voice reference if the draft risks generic AI cadence.

## Step 3: Retrieve patterns

Use pattern IDs from retrieval output and the brief.

For each selected example, extract:

- opening move,
- proof move,
- structure move,
- voice move,
- closing move,
- anti-pattern to avoid.

## Step 4: Build the brief

Run:

```bash
prosekernel brief "<task>" --mode hybrid --output /tmp/prosekernel-brief.md
```

The brief is provider-agnostic and does not call a model. It packages retrieved examples, pattern instructions, craft moves, and quality gates for any agent.

## Step 5: Draft

Write original text. Transfer structure, not phrases.

Rules:

- Lead with the reader's concrete situation, tension, proof, or a scene.
- Use proof before praise.
- Prefer concrete nouns and active verbs.
- Delete any sentence that could describe another product, company, or topic.
- Do not copy source phrases.

## Step 6: Evaluate

Run:

```bash
prosekernel lint draft.md
prosekernel scorecard draft.md --task "<task>"
prosekernel critique draft.md --task "<task>" --mode hybrid --output critique.md
```

Also use:

- `docs/anti-slop.md`
- `evals/writing-scorecard.md`
- relevant `patterns/*.md`

## Step 7: Revise

Perform manually or use the deterministic rewrite report as a working draft:

```bash
prosekernel rewrite draft.md --task "<task>" --mode hybrid --output rewrite.md --rewrite-output rewritten.md
```

Revision passes:
1. cut pass,
2. specificity pass,
3. proof pass,
4. structure pass,
5. voice/rhythm pass,
6. read-aloud pass.

## Step 8: Explain what changed

Return the final draft plus:

- retrieval/examples used,
- patterns applied,
- structure changes,
- proof/specificity changes,
- cuts made,
- lint/scorecard result,
- remaining risks or manual follow-ups.

## Step 9: Learn only when explicit and public-safe

Do not auto-save private user writing or model outputs as reusable lessons. If the user or maintainer explicitly wants to preserve a reusable lesson, create a metadata-only note:

```bash
prosekernel learn draft.md \
  --task "<task>" \
  --source-title "<title>" \
  --source-author "<author/company>" \
  --source-url "<url>" \
  --rights metadata-only \
  --category technical-explanatory \
  --tags "docs, clarity"

prosekernel validate-learning
```

The learning note must not store source prose. Promotion into examples or patterns requires safe rights and explicit human approval.
