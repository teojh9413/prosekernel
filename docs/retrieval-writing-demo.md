# Retrieval + Writing Demo

The retrieval demo turns ProseKernel from a static library into a writing workflow.

## Flow

1. Receive a writing task.
2. Recommend categories from the taxonomy.
3. Retrieve 3-5 annotated examples.
4. Extract craft moves from those examples.
5. Generate a local deterministic draft scaffold.
6. Run the anti-slop linter.
7. Score the draft with the Phase 7A scorecard.
8. Rewrite or annotate the draft based on lint results.
9. Return a markdown report with lint and scorecard improvement.

This workflow is local-first. Default retrieval is deterministic lexical/category scoring. Optional Phase 8 modes add offline semantic or hybrid scoring without paid APIs, embedding services, or runtime dependencies.

## Commands

Search for examples:

```bash
PYTHONPATH=src python3 -m prosekernel.cli search-examples "write a launch email for a new AI writing library" --limit 5
```

Search with optional hybrid retrieval and score explanation:

```bash
PYTHONPATH=src python3 -m prosekernel.cli search-examples "write a security incident update for customers" --mode hybrid --explain --limit 5
```

Run the full demo:

```bash
PYTHONPATH=src python3 -m prosekernel.cli write-demo "write a launch email for ProseKernel" --output /tmp/prosekernel-demo.md
```

Constrain retrieval to a category:

```bash
PYTHONPATH=src python3 -m prosekernel.cli write-demo "write an outage apology" --category crisis-communications
```

If a selected category has no examples yet, omit `--category` and let retrieval fall back to populated neighboring categories.

## Current limitation

The generated `write-demo` draft is a scaffold, not final prose. Provider-backed `prosekernel write` exists for explicit, user-selected LLM calls, but ProseKernel still refuses to choose a paid provider by default. Later retrieval upgrades may add true embeddings, but should preserve the current hybrid score breakdown and default lexical contract.
