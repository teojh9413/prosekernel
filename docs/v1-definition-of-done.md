# ProseKernel v1 Definition of Done

ProseKernel v1 is the end of the official numbered roadmap.

At v1, ProseKernel is an open-source writing operating system for AI agents: taste infrastructure that helps agents retrieve examples, apply patterns, build briefs, draft with structure, detect generic AI slop, rewrite with specificity and proof, explain changes, and preserve reusable lessons through explicit public-safe review.

## v1 is complete when a user can

1. Install the package.
2. Run it on a serious writing task.
3. Generate a writing brief.
4. Generate or evaluate a draft.
5. Receive a structured critique.
6. Receive a rewrite.
7. See the examples and patterns used.
8. Understand why the output improved.
9. Run validation and tests successfully.

## v1 does not require

- web UI
- MCP server
- editor plugin
- local model support
- hundreds of examples
- automatic library growth
- fully automated corpus growth
- complex benchmark suite
- PyPI publishing before the core loop is credible

## Stop Building Rule

Do not expand the roadmap just because more features are possible.

ProseKernel should be considered v1-complete when it can reliably help an agent produce a better writing brief, critique, and rewrite than a generic LLM workflow.

After that, new work must fit into one of the Post-v1 Tracks and should improve stability, distribution, evaluation, or clearly demonstrated user value.

## Post-v1 boundary

Post-v1 tracks are planning buckets, not permission to start every future surface.

The first practical post-v1 priorities are:

1. Structured Outputs / Agent API.
2. CI, Release, and Package Hardening.
3. Public Distribution.

Do not start web UI, MCP server, editor plugins, local model support, huge benchmark systems, automatic corpus growth, or large corpus expansion unless there is a clear user-value reason and the core v1 docs remain stable.
