# Retrieval + Writing Demo

The retrieval demo turns Humanprint from a static library into a writing workflow.

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

This first version is deterministic and local. It does not call a paid model. It is meant to prove the operating loop before adding LLM drafting.

## Commands

Search for examples:

```bash
PYTHONPATH=src python3 -m humanprint.cli search-examples "write a launch email for a new AI writing library" --limit 5
```

Run the full demo:

```bash
PYTHONPATH=src python3 -m humanprint.cli write-demo "write a launch email for Humanprint" --output /tmp/humanprint-demo.md
```

Constrain retrieval to a category:

```bash
PYTHONPATH=src python3 -m humanprint.cli write-demo "write an outage apology" --category crisis-communications
```

If a selected category has no examples yet, omit `--category` and let retrieval fall back to populated neighboring categories.

## Current limitation

The generated draft is a scaffold, not final prose. The next stage should add an LLM-backed drafting adapter that uses the retrieved examples, pattern IDs, craft moves, and scorecard as context while preserving the same lint/rewrite/report contract.
