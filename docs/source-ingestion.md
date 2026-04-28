# Source Ingestion Protocol

Use this whenever adding a new Humanprint example.

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

## 2. Classify rights

Use one of:

- `public-domain`
- `open-license`
- `short-excerpt`
- `metadata-only`
- `user-provided`

For modern copyrighted work, default to `metadata-only` and write original analysis.

## 3. Create the file

Use the CLI skeleton generator:

```bash
humanprint new-example \
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

## 6. Verify

Run:

```bash
humanprint validate-library
python3 -m pytest -q
```
