# Public Release Checklist

Use this checklist before making the ProseKernel repository public or tagging a v1 release candidate.

## Required checks

- [ ] CI passes on GitHub for every configured Python version.
- [ ] Local tests pass:

  ```bash
  python -m pytest -q
  ```

- [ ] Library validation passes:

  ```bash
  prosekernel validate-library --root .
  ```

- [ ] Learning-note validation passes:

  ```bash
  prosekernel validate-learning --root .
  ```

- [ ] Fixture evals pass:

  ```bash
  prosekernel eval --root .
  ```

- [ ] Old-brand scan passes. The test suite must reject tracked text references to the previous project name or old module path.
- [ ] README quickstart works from a fresh editable install.
- [ ] Repo can be made public without exposing private/user-specific content.
- [ ] `LICENSE` exists and uses MIT.
- [ ] `CONTRIBUTING.md` exists and explains acceptable examples, source URLs, rights classification, craft moves, and anti-patterns.
- [ ] No private/user-specific content is present in docs, examples, prompts, tests, proposals, or learning notes.
- [ ] No copyrighted full-text corpus is stored. Modern sources must use source metadata, links, short rights-safe excerpts only when appropriate, and original craft analysis.

## Manual spot-checks

Run a small v1 loop before release:

```bash
prosekernel brief "write a launch email for ProseKernel" --root . --output /tmp/prosekernel-brief.md
prosekernel search-examples "write a launch email for ProseKernel" --root . --limit 3
prosekernel validate-library --root .
prosekernel validate-learning --root .
prosekernel eval --root .
```

Confirm generated learning/proposal files, if any, contain:

- `source_text_stored: false`
- `proposal_status: review-required` for proposals
- no copied source prose
- no private credentials, personal notes, or user-specific operational details

## Release boundary

The v1 public-release boundary is CLI + Markdown/docs + repo-local library/pattern/eval assets. Do not treat public-release readiness as permission to add a web UI, MCP server, editor plugin, local model support, or a Phase 13 roadmap entry.
