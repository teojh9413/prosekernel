# ProseKernel

Taste infrastructure for AI writing agents.

ProseKernel is an open-source, repo-local CLI and knowledge layer that helps agents write with taste: retrieve relevant examples, apply craft patterns, catch generic AI slop, score drafts, produce critique/rewrite reports, and learn safely without storing private source prose.

## What ProseKernel does

- retrieves rights-safe writing examples
- extracts reusable craft patterns
- builds agent-ready writing briefs
- detects generic AI slop
- scores drafts with a deterministic writing scorecard
- produces critique/rewrite reports
- learns safely through metadata-only notes and human-reviewed proposals

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
prosekernel lint examples/ai-slop-sample.md
prosekernel eval
```

You can also run the public demo script:

```bash
bash scripts/public_demo.sh
```

Commands can run from the repo root, with `--root /path/to/prosekernel`, or with `PROSEKERNEL_ROOT=/path/to/prosekernel`. See [`docs/install.md`](docs/install.md) for local install and root-resolution details.

## Sample reports

- [See sample brief](examples/reports/launch-email-brief.md)
- [See sample critique](examples/reports/slop-critique-report.md)
- [See sample rewrite](examples/reports/rewrite-report.md)

## Why this exists

Most AI writing is not bad because it is grammatically wrong. It is bad because it is:

- generic
- over-smoothed
- overconfident without proof
- inflated with fake importance
- formatted like an answer instead of written like a human
- full of phrases no serious writer would choose

ProseKernel is designed to make future agents pause, study, retrieve relevant examples, and write with taste.

## How agents should use this repo

Before writing anything important:

1. Read `docs/doctrine.md`.
2. Open `LIBRARY.md` and find 3-5 relevant examples.
3. Read the example annotations, not just the excerpts.
4. Extract structure and craft moves. Do **not** copy phrases.
5. Build a brief with `prosekernel brief`.
6. Draft.
7. Run `prosekernel lint` and `prosekernel scorecard`.
8. Use `prosekernel critique` / `prosekernel rewrite` for deterministic revision guidance.

## Install / local usage

Install ProseKernel from the repo root with:

```bash
python -m pip install -e .
```

Most commands can be run from the repo root directly. If you run the installed CLI from another directory, pass `--root /path/to/prosekernel` or set `PROSEKERNEL_ROOT=/path/to/prosekernel` so ProseKernel can find `library/`, `patterns/`, and `evals/`.

See [`docs/install.md`](docs/install.md) for full local usage and root-resolution details.

## Quick CLI

```bash
python -m pip install -e .
prosekernel lint examples/ai-slop-sample.md
prosekernel search-examples "write a launch email for ProseKernel"
prosekernel examples "write a launch email for ProseKernel"
prosekernel search-examples "write a security incident update for customers" --mode hybrid --explain
prosekernel brief "write a launch email for ProseKernel" --output /tmp/prosekernel-brief.md
prosekernel critique draft.md --task "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-critique.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --mode hybrid --output /tmp/prosekernel-rewrite.md
prosekernel rewrite draft.md --task "write a launch email for ProseKernel" --output /tmp/prosekernel-rewrite-report.md --rewrite-output /tmp/prosekernel-rewritten.md
prosekernel learn draft.md --task "write a launch email for ProseKernel" --source-title "Launch draft" --source-author "User" --source-url "https://example.com/launch-draft" --rights user-provided --category email-newsletters --tags "launch, email" --promote --approved --output /tmp/prosekernel-lesson.md
prosekernel validate-learning
prosekernel propose-example /tmp/prosekernel-lesson.md --root /root/prosekernel --output /tmp/prosekernel-example-proposal.md
prosekernel propose-pattern /tmp/prosekernel-lesson.md --root /root/prosekernel --pattern-id PATTERN_EMAIL_999 --output /tmp/prosekernel-pattern-proposal.md
prosekernel write "write a launch email for ProseKernel" --provider openai --model gpt-4o-mini --output /tmp/prosekernel-write.md
prosekernel write-demo "write a launch email for ProseKernel" --output /tmp/prosekernel-demo.md
prosekernel demo "write a launch email for ProseKernel" --output /tmp/prosekernel-demo.md
prosekernel scorecard draft.md --task "write a launch email for ProseKernel" --output /tmp/prosekernel-scorecard.md
prosekernel score draft.md --task "write a launch email for ProseKernel"
prosekernel eval
```

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

Track B release hardening is mostly implemented: root resolution, CI, validation hardening, old-brand scan, install docs, public-release checklist, and the v1 smoke-loop test are complete.

Track C public launch prep is in progress: README clarity, sample reports, a public demo script, changelog, release-process docs, and GitHub release settings are being prepared for public v1.

Seed corpus includes 100 annotated examples across 12 populated categories and 12 strict pattern families. This is intentionally high-signal. Quality beats volume.

Corpus depth rule: one example gives a direction; three to five examples create a pattern; ten examples create taste.

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

Use `docs/retrieval-writing-demo.md` for the current workflow: task → category recommendation → example retrieval → craft move extraction → draft scaffold → anti-slop lint → scorecard → rewrite/report. Use `docs/phase-12-human-review-import-bridge.md` for generating review-required example/pattern proposals from approved learning notes. Use `docs/phase-11-public-safe-learning-loop.md` for metadata-only learning notes and safe promotion gates. Use `docs/phase-10-productized-cli.md` for deterministic critique/rewrite reports, standalone rewrite outputs, exit-code semantics, and short CLI aliases. Use `docs/phase-8-hybrid-retrieval.md` for optional offline semantic/hybrid retrieval modes. Use `docs/phase-9-agent-workflow.md` and `docs/agent-workflow.md` for the full agent loop: classify → retrieve → patterns → brief → draft → lint/score → revise → explain. Use `docs/phase-7a-evals.md` for the fixture suite and scorecard CLI. Use `docs/phase-6-brief-mode.md` for the provider-agnostic dry-run brief mode and `docs/phase-6b-provider-write.md` for explicit provider write mode.
