# ProseKernel Writing Brief Prompt

Use this template to turn a user request into an agent-ready writing brief.

## Inputs to collect

- Reader:
- Goal:
- Awareness stage:
- Format/channel:
- Required facts:
- Proof available:
- Desired action:
- Voice constraints:
- Forbidden language:
- Length/structure constraints:

## Retrieval packet

Run or request:

```bash
prosekernel brief "<task>" --mode hybrid --output /tmp/prosekernel-brief.md
```

Then fill:

## Reader

Who is reading this, what do they already believe, and what pressure are they under?

## Goal

What should the reader understand, feel, decide, or do after reading?

## Awareness stage

Unaware, problem-aware, solution-aware, product-aware, or most-aware. Explain why.

## Retrieved examples

List 3-5 examples and why each matters:

- Example:
  - Format/goal relevance:
  - Craft moves to transfer:
  - What not to copy:

## Patterns to apply

List pattern IDs and convert each into direct drafting instructions.

## Structure plan

- Opening move:
- Proof sequence:
- Body structure:
- Objection/reader-risk handling:
- Closing move:

## Drafting rules

- Do structure transfer, not phrase transfer.
- Use proof before praise.
- Prefer concrete nouns and active verbs.
- Replace generic claims with named details, examples, constraints, mechanisms, or numbers.
- Cut any sentence that could apply to another product, company, or topic.

## Quality gate

Before publishing, run:

```bash
prosekernel lint draft.md
prosekernel scorecard draft.md --task "<task>"
```

The draft is not ready until it shows specificity, proof, structure, reader fit, memorability, and non-genericness.
