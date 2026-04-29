# Humanprint

**Give AI writing a fingerprint.**

Humanprint is an open-source writing taste layer for AI agents. It helps agents retrieve strong writing examples, extract reusable craft patterns, draft with structure, and detect generic AI slop before publishing.

The system has four layers:

1. **Library** — annotated examples of excellent writing across formats.
2. **Patterns** — reusable craft moves extracted from the examples.
3. **Doctrine** — rules for clear, specific, persuasive, human writing.
4. **Evals** — anti-slop checks that catch fake significance, generic claims, weak proof, and AI cadence.

Humanprint preserves source metadata, summarizes what matters, extracts craft concepts, connects related ideas, and turns writing knowledge into reusable operating rules for agents.

## Why this exists

Most AI writing is not bad because it is grammatically wrong. It is bad because it is:

- generic
- over-smoothed
- overconfident without proof
- inflated with fake importance
- formatted like an answer instead of written like a human
- full of phrases no serious writer would choose

Humanprint is designed to make future agents pause, study, retrieve relevant examples, and write with taste.

## How agents should use this repo

Before writing anything important:

1. Read `docs/doctrine.md`.
2. Open `LIBRARY.md` and find 3-5 relevant examples.
3. Read the example annotations, not just the excerpts.
4. Extract structure and craft moves. Do **not** copy phrases.
5. Draft.
6. Run the anti-slop checklist in `docs/anti-slop.md`.
7. Score the draft with `evals/writing-scorecard.md`.

## Current status

Phase 3.5 is complete: public-release metadata/docs are in place after taxonomy expansion, retrieval demo, and seeded expanded categories.

Seed corpus includes examples/resources across:

- viral/social writing
- persuasive copywriting
- strategic/intelligent writing
- essay/literary craft
- technical/explanatory writing
- brand/positioning writing

Seed examples now exist for email/newsletters, speeches/oratory, journalism/reportage, UX/product microcopy, crisis communications, and internal ops docs.

This is intentionally small and high-signal. Quality beats volume.

## Quick CLI

The repo also includes a simple linter for common AI-slop markers:

```bash
python -m pip install -e .
humanprint lint examples/ai-slop-sample.md
humanprint search-examples "write a launch email for Humanprint"
humanprint write-demo "write a launch email for Humanprint" --output /tmp/humanprint-demo.md
```

## Core standard

Good Humanprint writing must be:

- **clear** — the reader understands the point fast
- **specific** — claims have names, numbers, examples, or scenes
- **alive** — it sounds like a person with judgment wrote it
- **persuasive** — structure fits reader awareness and desired action
- **honest** — no fake certainty, fake citations, or inflated importance


## Public source policy

Humanprint teaches structure, taste, and craft. It is not a copyrighted text mirror.

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

See `ROADMAP.md`. The build order is: public readiness → corpus depth → patterns → basic evals → LLM adapter → hybrid retrieval → agent workflow → productized CLI → public-safe learning loop.

## Source ingestion

Use `docs/source-ingestion.md` and `humanprint new-example` to add new examples safely and consistently. Run `humanprint validate-library` before committing.

## Retrieval + writing demo

Use `docs/retrieval-writing-demo.md` for the current deterministic workflow: task → category recommendation → example retrieval → craft move extraction → draft scaffold → anti-slop lint → rewrite/report.
