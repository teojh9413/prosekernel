# Source Ingestion Protocol

Use this whenever adding a new ProseKernel example.

## 1. Screen the candidate

Admit only if it teaches a reusable craft move:

- unforgettable opening
- clear explanation
- proof chain
- elegant structure
- memorable metaphor
- persuasion density
- strategic framing
- distinctive voice
- compression

Popularity alone is not enough.

For public contributions, also check `docs/example-quality-rubric.md` and `CONTRIBUTING.md`.

## 2. Classify rights

Use one of:

- `public-domain`
- `open-license`
- `short-excerpt`
- `metadata-only`
- `user-provided`

For modern copyrighted work, default to `metadata-only` and write original analysis. If you are learning from a draft but are not ready to add a library example, use `prosekernel learn` instead of `new-example`; it stores metadata, hash, metrics, and lessons without storing source prose. If a learning note is later approved with safe rights, use `prosekernel propose-example` or `prosekernel propose-pattern` to create a review-required proposal under `proposals/`; do not import it directly.

## 3. Create the file

Use the CLI skeleton generator:

```bash
prosekernel new-example \
  --title "Example Title" \
  --author "Author" \
  --source-url "https://example.com" \
  --date-published "2026" \
  --added "2026-04-28" \
  --category viral-social \
  --format thread \
  --rights metadata-only \
  --tags hook,proof,clarity \
  --quality-score 8 \
  --use-when "When an agent needs to..."
```

## 4. Fill every section

Required:

- Source
- Why this is good
- Craft moves
- Structure map
- Excerpt or summary
- Reusable pattern
- Imitation prompt
- Anti-patterns to avoid

## 5. Update navigation

Update:

- `LIBRARY.md`
- relevant `library/<category>/index.md`
- relevant `patterns/*.md` if the example reveals a new reusable move

## 6. Optional safe learning note

If the source is useful as a lesson but should not become a library example yet, create a metadata-only learning note:

```bash
prosekernel learn draft.md \
  --task "what this source teaches" \
  --source-title "Example Title" \
  --source-author "Author" \
  --source-url "https://example.com" \
  --rights metadata-only \
  --category technical-explanatory \
  --tags "docs, clarity"

prosekernel validate-learning
```

Do not promote learning notes into examples or patterns unless rights are safe and human approval is explicit.

## 7. Optional reviewed proposal

If a learning note is approved and rights are safe (`public-domain`, `open-license`, or `user-provided`), generate a proposal instead of importing directly:

```bash
prosekernel propose-example learning/lessons/<note>.md --root /root/prosekernel
prosekernel propose-pattern learning/lessons/<note>.md --root /root/prosekernel --pattern-id PATTERN_DOMAIN_001
```

Keep the generated file under `proposals/` until a human replaces review-required placeholders with original analysis and confirms there is no duplicate or unsafe import.

## 8. Verify

Run:

```bash
prosekernel validate-library
prosekernel validate-learning
python3 -m pytest -q
```
