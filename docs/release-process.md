# Release Process

Use this checklist to cut the public v1 release after GitHub CI passes on `main`.

## Pre-release verification

Run from the repository root:

```bash
python -m pytest -q
prosekernel validate-library --root .
prosekernel validate-learning --root .
prosekernel eval --root .
bash scripts/public_demo.sh
git diff --check
```

Expected result:

- tests pass
- library validation passes
- learning validation passes
- fixture eval passes
- public demo script runs end-to-end
- diff check is clean

## Tagging

After verification and a clean working tree, create and push the v1 public tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

## GitHub release

Release title:

```text
ProseKernel v0.1.0 — Public v1
```

Release summary:

```text
ProseKernel is taste infrastructure for AI writing agents: a repo-local CLI and knowledge layer for retrieval, writing briefs, anti-slop checks, scorecards, critique/rewrite reports, and public-safe learning.
```

## Stop rule

After public v1 launch, stop building by default. Do not add Phase 13 or new product surfaces unless there is explicit user demand and the work fits a Post-v1 Track.
