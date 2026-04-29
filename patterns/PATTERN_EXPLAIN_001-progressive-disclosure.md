# PATTERN_EXPLAIN_001 — Progressive disclosure explanation

## Use when
Use this pattern for technical docs, tutorials, explainers, onboarding guides, architecture notes, and any writing that must teach a complex concept without overwhelming the reader.

## Reader situation
The reader wants to do or understand something, but the domain has too many terms, dependencies, and edge cases. They need a path, not a wall of complete information.

## Structure
1. Start with the reader’s task or mental model, not the system’s internal taxonomy.
2. Give the smallest useful concept that unlocks the next step.
3. Show one concrete example before introducing edge cases.
4. Layer concepts in dependency order.
5. Separate tutorial, reference, explanation, and how-to material when the reader’s need changes.
6. Offer deeper detail only after the reader has a working scaffold.

## Why it works
Complex writing fails when it tries to be complete before it is usable. Progressive disclosure protects working memory. It gives the reader enough structure to move forward, then reveals complexity at the moment it becomes meaningful.

## Examples
- `library/technical-explanatory/examples/diataxis-documentation-framework.md` — organizes documentation by user need instead of dumping all information together.
- `library/technical-explanatory/examples/django-polls-tutorial-incremental-app.md` — uses a small real app to teach framework concepts in sequence.
- `library/technical-explanatory/examples/rust-book-ownership-chapter.md` — names the mental model before edge cases.
- `library/technical-explanatory/examples/mdn-using-fetch-api-task-first-explanation.md` — teaches an API through tasks developers actually try to do.
- `library/technical-explanatory/examples/stripe-docs-progressive-disclosure.md` — uses examples, hierarchy, and reader control to make integration approachable.

## Anti-patterns
- Starting with definitions before the reader knows why they matter.
- Explaining every exception before the normal path is clear.
- Mixing tutorial, reference, and conceptual explanation in the same section.
- Organizing docs around the system’s architecture instead of the reader’s sequence of understanding.
- Mistaking completeness for clarity.

## Agent instruction
When explaining a complex topic, write the learning ladder first: task → first concept → example → next concept → edge cases. Draft only one rung at a time, and move advanced detail later unless it is required for the current step.
