# Phase 8 — Hybrid / Semantic Retrieval

Phase 8 adds an optional hybrid retrieval scorer while preserving the default deterministic lexical/category contract.

## Goals

- Keep ProseKernel local, offline, and dependency-free by default.
- Preserve existing CLI output unless a user explicitly asks for a new retrieval mode or score explanation.
- Improve retrieval for tasks where the user describes intent with adjacent language instead of exact category keywords.
- Keep category, tag, pattern, keyword, semantic intent, and quality signals visible rather than hiding ranking behind opaque vector search.

## Retrieval modes

`prosekernel search-examples`, `prosekernel brief`, `prosekernel write`, and `prosekernel write-demo` accept:

- `--mode lexical` — default. Existing deterministic scoring: category preference, keyword/tag/pattern overlap, and quality score.
- `--mode semantic` — offline concept matching using curated aliases and category concepts.
- `--mode hybrid` — lexical score plus semantic score.

Examples:

```bash
PYTHONPATH=src python3 -m prosekernel.cli search-examples "write a security incident update for customers" --mode hybrid --explain
PYTHONPATH=src python3 -m prosekernel.cli brief "write a customer trust update after a compromised credential scare" --mode hybrid --output /tmp/prosekernel-brief.md
PYTHONPATH=src python3 -m prosekernel.cli write-demo "write an outage apology" --mode hybrid --output /tmp/prosekernel-demo.md
```

## Explain output

`search-examples --explain` prints the selected mode plus score components:

```text
Retrieval mode: hybrid
- Example title [category] patterns: PATTERN_... library/... lexical=48 semantic=31 hybrid=79
```

This keeps ranking auditable for agents and humans.

## Offline semantic approach

The Phase 8 semantic layer is intentionally lightweight:

- Curated concept aliases map intent words such as `trust`, `security`, `crisis`, `decision`, `internal`, `speech`, `journalism`, `email`, `ux`, `proof`, `brand`, and `technical` to adjacent terms.
- Category concepts connect each top-level writing category to likely intent clusters.
- Simple stemming catches close variants without adding NLP dependencies.
- Semantic token expansion is cached in-process with `functools.lru_cache`.

No embedding API, paid provider, network call, model download, database, or heavyweight runtime dependency is introduced.

## Contract preservation

Default commands still behave as before:

```bash
PYTHONPATH=src python3 -m prosekernel.cli search-examples "write a launch email for ProseKernel"
PYTHONPATH=src python3 -m prosekernel.cli brief "write a launch email for ProseKernel"
PYTHONPATH=src python3 -m prosekernel.cli write-demo "write a launch email for ProseKernel"
```

Reports now include `Retrieval mode: ...` for traceability. The default is `lexical`, so existing category-first deterministic behavior remains stable.

## Future upgrades

If ProseKernel later adds true embeddings, keep the hybrid architecture:

1. lexical/category score,
2. tag/pattern score,
3. semantic/vector score,
4. quality score,
5. explainable score breakdown.

Do not replace the current retrieval stack with opaque pure vector search.
