# Humanprint Taxonomy

Humanprint uses categories to help agents retrieve the right craft examples before drafting. The taxonomy is deliberately small enough to stay usable and broad enough to cover real writing work.

## Rule

Add a top-level category only when the writing mode has a distinct reader situation, structure, and quality bar. If a format is blended, keep it as a subcategory or tag under the nearest parent.

## Core populated categories

- `viral-social` — hooks, compression, rhythm, shareability, threads, short posts.
- `persuasive-copywriting` — landing pages, sales emails, offers, objections, proof, conversion.
- `strategic-intelligent` — memos, theses, annual letters, investor logic, executive tradeoffs.
- `essays-literary` — voice, clarity, scene, rhythm, argument, literary nonfiction.
- `technical-explanatory` — docs, tutorials, explainers, progressive disclosure, user education.
- `brand-positioning` — manifestos, category pages, slogans, worldview, memorable positioning.

## New target top-level categories

- `email-newsletters` — launch emails, lifecycle sequences, founder updates, editorial newsletters.
- `speeches-oratory` — keynotes, public remarks, civic rhetoric, ceremonial speeches.
- `journalism-reportage` — profiles, interviews, investigations, reported features.
- `ux-product-microcopy` — onboarding, empty states, errors, labels, tooltips, product flows.
- `crisis-communications` — apologies, incident notes, recalls, postmortems, trust repair.
- `internal-ops-docs` — SOPs, decision records, internal memos, one-pagers, runbooks.

## Blended formats: use tags/subcategories

- Fundraising, investor decks, grant proposals → `strategic-intelligent` + `persuasive-copywriting`.
- Customer support, community, moderation → `ux-product-microcopy` or `crisis-communications`.
- Scripts, video narration, podcasts → `essays-literary` or `viral-social`.
- Academic, legal, policy → `strategic-intelligent`.
- Sales enablement, case studies, whitepapers → `persuasive-copywriting` + `technical-explanatory`.
- Criticism, reviews, cultural analysis → `essays-literary` + `journalism-reportage`.

## Retrieval behavior

`humanprint search-examples` and `humanprint write-demo` use keyword/category heuristics. New categories can be recommended even before they have examples; until populated, retrieval falls back to the closest populated categories.
