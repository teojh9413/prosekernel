# ProseKernel

Taste infrastructure for AI writing agents.

ProseKernel is a local writing-quality layer for AI agents.

It helps an agent study rights-safe examples, apply reusable writing patterns, catch generic AI slop, diagnose default AI document structure, score drafts, and produce critique/rewrite reports before publishing.

## What ProseKernel does

- Retrieves rights-safe writing examples.
- Extracts reusable craft patterns.
- Builds agent-ready writing briefs.
- Detects generic AI slop.
- Diagnoses AI-looking document structure with editorial architecture checks.
- Scores drafts with deterministic scorecards.
- Produces critique, rewrite, and shape reports.
- Learns safely through metadata-only notes and human-reviewed proposals.

## Who it is for

- AI coding agents
- writing agents
- founders/operators using agents for serious writing
- maintainers building agent workflows
- anyone who wants a local anti-slop writing quality layer

## 60-second demo

Run from the repo root:

```bash
python -m pip install -e .
prosekernel brief "write a launch email for an AI writing tool" --output /tmp/prosekernel-brief.md
prosekernel search-examples "write a launch email for an AI writing tool" --limit 3
prosekernel shape examples/ai-structure-sample.md --task "proposal to payments company" --reader "company boss" --intent "create curiosity for a meeting"
prosekernel lint examples/ai-slop-sample.md || true
prosekernel eval
```

The lint command intentionally flags the sample draft; that is the point of the demo.

You can also run the public demo script:

```bash
bash scripts/public_demo.sh
```

Commands can run from the repo root, with `--root /path/to/prosekernel`, or with `PROSEKERNEL_ROOT=/path/to/prosekernel`. See [`docs/install.md`](docs/install.md) for local install and root-resolution details.

## Sample reports

- [See sample brief](examples/reports/launch-email-brief.md)
- [See sample critique](examples/reports/slop-critique-report.md)
- [See sample rewrite](examples/reports/rewrite-report.md)
- [See sample shape report](examples/reports/shape-report.md)

## Why this exists

Most AI writing is not bad because it is ungrammatical.

It is bad because it sounds finished before it has judgment: generic claims, weak proof, inflated importance, and sentences that could describe any product.

ProseKernel gives agents a writing loop:

```text
retrieve examples → apply patterns → draft → shape → lint → score → critique → rewrite → learn safely
```

## Editorial architecture

Good AI-assisted writing is not only about better sentences.
A draft can be polished and still look AI generated if it follows a default article or proposal skeleton.

ProseKernel includes an editorial architecture layer to diagnose document shape before sentence polish. It checks for generic section ladders, over-balanced rhythm, excessive one-sentence paragraphs, repeated contrast formulas, em dash overuse, weak endings, fake completeness, topic-container headings, and structures that do not fit the reader or intent.

```bash
prosekernel shape draft.md \
  --task "proposal to payments company" \
  --reader "company boss" \
  --intent "create curiosity for a meeting" \
  --output shape-report.md
```

The shape command is diagnostic, not a hard quality gate. It does not claim to make writing undetectable. It is about better editorial judgment: choosing the right document shape for the reader, intent, and situation.

See [`docs/editorial-architecture.md`](docs/editorial-architecture.md) for the full concept and archetypes.

Important positioning:

Do **not** say ProseKernel helps users evade AI detection.
Do **not** market this as “make AI writing undetectable.”
Frame it as better editorial judgment and better structure.

## How agents should use this repo

Before writing anything important:

1. Run `brief` to retrieve examples, patterns, and writing guidance.
2. Draft with the retrieved examples and patterns in context.
3. Run `shape` to check whether the document architecture fits the reader and intent.
4. Run `lint` and `scorecard` to catch generic AI slop and weak proof.
5. Run `critique` or `rewrite` to generate a report and revised draft.
6. Use `learn` only for metadata-only notes. Do not store private source prose.
7. Use `propose-example` or `propose-pattern` only for human-reviewed imports.

## Install / local usage

Install ProseKernel from the repo root with:

```bash
python -m pip install -e .
```

Most commands can be run from the repo root directly. If you run the installed CLI from another directory, pass `--root /path/to/prosekernel` or set `PROSEKERNEL_ROOT=/path/to/prosekernel` so ProseKernel can find `library/`, `patterns/`, and `evals/`.

See [`docs/install.md`](docs/install.md) for full local usage and root-resolution details.

## Common commands

```bash
prosekernel brief "write a launch email for an AI writing tool"
prosekernel search-examples "write a security incident update" --mode hybrid --explain
prosekernel shape draft.md --task "proposal to payments company" --reader "company boss" --intent "create curiosity for a meeting"
prosekernel critique draft.md --task "write a launch email"
prosekernel rewrite draft.md --task "write a launch email" --rewrite-output rewritten.md
prosekernel scorecard draft.md --task "write a launch email"
prosekernel eval
```

For full workflows, provider-backed drafting, editorial architecture, learning notes, and human-review proposals, see [`docs/install.md`](docs/install.md), [`docs/retrieval-writing-demo.md`](docs/retrieval-writing-demo.md), [`docs/editorial-architecture.md`](docs/editorial-architecture.md), [`docs/phase-10-productized-cli.md`](docs/phase-10-productized-cli.md), [`docs/phase-11-public-safe-learning-loop.md`](docs/phase-11-public-safe-learning-loop.md), and [`docs/phase-12-human-review-import-bridge.md`](docs/phase-12-human-review-import-bridge.md).

Root-aware commands resolve the ProseKernel repo/data root in this order: explicit `--root`, `PROSEKERNEL_ROOT`, then an upward search from the current directory for `pyproject.toml`, `library/`, `patterns/`, and `src/prosekernel`. If installed usage cannot find those assets, ProseKernel fails with a clear setup message instead of returning empty retrieval results.

## Core standard

Good ProseKernel writing must be:

- **clear** — the reader understands the point fast
- **specific** — claims have names, numbers, examples, or scenes
- **alive** — it sounds like a person with judgment wrote it
- **persuasive** — structure fits reader awareness and desired action
- **honest** — no fake certainty, fake citations, or inflated importance

## Current status

Phase 12 is the official v1 endgame: ProseKernel now covers the full writing operating-system loop for agents — task understanding, retrieval, patterns, briefs, critique, rewrite, explanation, public-safe learning, and a human-review/import bridge. Later work is organized as Post-v1 Tracks, not new numbered phases.

Implemented layers include retrieval, pattern-backed briefs, linting, deterministic scorecards, critique/rewrite reports, public-safe learning, human-reviewed proposal generation, and editorial architecture shape diagnostics.

Track A structured outputs / agent API is planned. Do not treat structured JSON outputs as implemented.

Track B release hardening is mostly implemented: root resolution, CI, validation hardening, old-brand scan, install docs, public-release checklist, and the v1 smoke-loop test are complete.

Track C public launch prep is implemented: README clarity, sample reports, public demo script, changelog, release-process docs, and GitHub release settings are ready for public v1.

Track H editorial architecture is implemented: `prosekernel shape` diagnoses document shape before sentence polish, recommends situated structure archetypes, and writes deterministic Markdown shape reports.

Seed corpus includes 100 annotated examples across 12 populated categories and 12 strict pattern families. This is intentionally high-signal. Quality beats volume.

Corpus depth rule: one example gives a direction; three to five examples create a pattern; ten examples create taste.

## Non-goals

ProseKernel is not:

- an AI-detection evasion tool;
- a way to claim AI-assisted writing was not AI-assisted;
- a copyrighted text mirror;
- a private voice clone;
- a web UI, MCP server, editor plugin, or local model runtime.

## Public source policy

ProseKernel teaches structure, taste, and craft. It is not a copyrighted text mirror.

For modern copyrighted writing, default to:

- source metadata
- source URL
- rights classification
- short excerpt only when legally appropriate
- original craft analysis
- reusable pattern
- imitation prompt

See `docs/legal-source-policy.md`, `docs/source-ingestion.md`, and `CONTRIBUTING.md`.

## Roadmap

See `ROADMAP.md` and `docs/v1-definition-of-done.md`. The official numbered roadmap ends at Phase 12: public readiness → corpus depth → patterns → basic evals → LLM adapter → hybrid retrieval → agent workflow → productized CLI → public-safe learning loop → human-review/import bridge → v1 Writing OS endgame. Later work belongs in Post-v1 Tracks for structured outputs, CI/release hardening, public distribution, evaluation maturity, library/pattern scale, provider support, and optional product surfaces.

## Source ingestion

Use `docs/source-ingestion.md` and `prosekernel new-example` to add new examples safely and consistently. Run `prosekernel validate-library` before committing.

## Retrieval + writing demo

Use `docs/retrieval-writing-demo.md` for the current workflow: task → category recommendation → example retrieval → craft move extraction → draft scaffold → shape diagnostics → anti-slop lint → scorecard → rewrite/report. Use `docs/editorial-architecture.md` for document shape diagnostics and situated structure archetypes. Use `docs/phase-12-human-review-import-bridge.md` for generating review-required example/pattern proposals from approved learning notes. Use `docs/phase-11-public-safe-learning-loop.md` for metadata-only learning notes and safe promotion gates. Use `docs/phase-10-productized-cli.md` for deterministic critique/rewrite reports, standalone rewrite outputs, exit-code semantics, and short CLI aliases. Use `docs/phase-8-hybrid-retrieval.md` for optional offline semantic/hybrid retrieval modes. Use `docs/phase-9-agent-workflow.md` and `docs/agent-workflow.md` for the full agent loop: classify → retrieve → patterns → brief → draft → shape → lint/score → revise → explain. Use `docs/phase-7a-evals.md` for the fixture suite and scorecard CLI. Use `docs/phase-6-brief-mode.md` for the provider-agnostic dry-run brief mode and `docs/phase-6b-provider-write.md` for explicit provider write mode.

## Core claim

> AI agents need a local taste and structure layer before their writing should be trusted.
