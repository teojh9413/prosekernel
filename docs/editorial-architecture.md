# Editorial Architecture

Good AI-assisted writing is not only about better sentences. A draft can be grammatical, polished, and still look AI generated because it inherited the model's default document skeleton.

ProseKernel's editorial architecture layer diagnoses document shape before sentence polish. It asks whether the piece is organized by reader, intent, situation, and decision, rather than by a generic article or proposal ladder.

```text
reader → intent → situation → document shape → sequence → emphasis → prose
```

The principle is simple:

```text
Do not let the default AI article skeleton decide the shape of the work.
```

## Better headings are not the same as better structure

A generic proposal can use more elegant headings and still be generic underneath. If the sequence is still executive summary → market opportunity → benefits → implementation → conclusion, the reader can feel the template even when every heading has been rewritten.

The shape command therefore does not only ask whether a heading sounds good. It asks whether the section belongs in that position, whether the document is trying to do too much, and whether the ending creates a decision or next action.

## Why ProseKernel cares about shape

ProseKernel already helps agents retrieve examples, apply patterns, lint generic prose, score drafts, critique, rewrite, and learn safely.

Editorial architecture adds the missing layer before prose polish:

```text
reader → intent → situation → document shape → sequence → emphasis → prose
```

A piece can pass sentence-level lint and still fail the reader because it used the wrong document shape. A founder note, decision brief, technical explainer, and curiosity proposal should not share the same skeleton.

## Common AI structure smells

ProseKernel currently checks deterministic signals first. No model call is required.

Common smells include:

1. Generic article ladders: Introduction, What is X, Why X matters, Key benefits, Challenges, Future outlook, Conclusion.
2. Generic proposal ladders: Executive Summary, Market Opportunity, Proposed Solution, Implementation Roadmap, Conclusion.
3. Over-balanced sections where every section has similar weight.
4. Too many one-sentence paragraphs creating artificial dramatic rhythm.
5. Frequent em dashes used as decorative sophistication.
6. Repeated contrast formulas such as "not X, but Y" or "the question is not X; the question is Y."
7. Generic signposting such as "In today's rapidly evolving landscape" or "It is important to note that."
8. Fake completeness: covering everything when the real goal is to create a meeting, decision, or sharper tradeoff.
9. Weak endings that only summarize instead of creating a next step, consequence, question, or judgment.
10. Topic-container headings such as Benefits, Challenges, Overview, Roadmap, or Conclusion.
11. Lack of situated reader, company, scenario, decision, or context.

## Structure archetypes

The first version supports seven deterministic archetypes.

### Direct Advisory Note

Use for a boss, founder, client, or senior decision maker.

Shape:

1. Why I am writing this
2. What I think the real issue is
3. What most people would do first
4. Why I think that is not enough
5. The path I would explore
6. What we should decide in conversation

### Curiosity Proposal

Use when the goal is to make the reader want a meeting, not to close the whole decision on paper.

Shape:

1. A quick observation
2. The opportunity behind it
3. Why this may matter for your company
4. Three possible directions
5. The one most worth discussing
6. What I would like to explore with you

### Strategic Memo

Use when the reader needs to understand a tradeoff or make a directional decision.

Shape:

1. The core thesis
2. The current constraint
3. The leverage point
4. The options
5. The tradeoff
6. The recommended move
7. The open questions

### Founder Narrative

Use when explaining why something was built.

Shape:

1. The frustration
2. The thing I kept noticing
3. The failed obvious solutions
4. The sharper insight
5. What I built
6. What it changes
7. Who should try it

### Decision Brief

Use when humans and agents need to decide or act.

Shape:

1. Decision needed
2. Recommendation
3. Evidence
4. Risks
5. Rejected alternatives
6. Next action

### Market Thesis Note

Use when making an argument about a category, trend, or strategic shift.

Shape:

1. The common reading
2. What that reading misses
3. The structural shift
4. Who gains power
5. Who loses power
6. What to watch next

### Technical Explainer with Judgment

Use when explaining a technical product without sounding like documentation or marketing copy.

Shape:

1. The user problem
2. The old way
3. Why the old way breaks
4. The new mechanism
5. What changes in practice
6. The limits
7. Where to start

## Run `prosekernel shape`

```bash
prosekernel shape draft.md \
  --task "proposal to payments company" \
  --reader "company boss" \
  --intent "create curiosity for a meeting" \
  --output shape-report.md
```

Options:

- `--task`: required. Describe the writing job or situation.
- `--reader`: optional but recommended. The diagnosis is less certain without it.
- `--intent`: optional but recommended. Describe what the piece should cause.
- `--channel`: optional. Add format or channel context.
- `--output`: optional. Writes a Markdown report.
- `--root`: optional. Allows installed CLI usage from outside the repo.

The command exits 0 when the report is generated. High AI structure risk is diagnostic, not a hard quality gate.

## Interpret the report

The report includes:

1. Overall AI structure risk.
2. A 0 to 100 shape scorecard.
3. Deterministic findings.
4. Automatic metrics.
5. Recommended structure archetype.
6. Rewrite instructions for another agent or a later rewrite command.

Score interpretation:

- 85 to 100: strong human architecture.
- 70 to 84: usable with minor structure polish.
- 55 to 69: clear but template-like.
- 40 to 54: high AI structure risk.
- 0 to 39: default AI document shape.

This layer is about better editorial judgment and structure. It is not marketed as making AI writing undetectable, and it should not encourage deception.
