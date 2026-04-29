# Humanprint Writing Scorecard

Score every important draft from 0-100. This scorecard is the human-readable half of Phase 7A: it catches "smart-sounding but empty" writing, not just obvious AI-slop phrases.

## Core dimensions

### 1. Specificity — 20 points

- 0-5: mostly abstractions, vibes, or category claims
- 6-10: some concrete examples, but generic claims still carry the piece
- 11-15: names, numbers, mechanisms, scenes, or constraints appear in most sections
- 16-20: concrete details do the persuasive work; the reader can picture or verify the claim

### 2. Proof — 20 points

- 0-5: claims without evidence
- 6-10: weak proof, fake precision, source-list theater, or examples that do not support the claim
- 11-15: credible evidence with a few unsupported jumps
- 16-20: proof chain makes the argument hard to ignore: claim → evidence → implication

### 3. Structure — 15 points

- 0-5: list-shaped mush, no progression
- 6-10: organized but predictable; sections could be rearranged without loss
- 11-15: structure creates momentum, contrast, reveal, accountability, or decision clarity

### 4. Reader fit — 15 points

- 0-5: wrong reader, wrong awareness stage, wrong level of context, or unclear ask
- 6-10: broadly relevant but not tuned to reader doubts, urgency, or constraints
- 11-15: message matches what the reader already knows, fears, wants, and needs next

### 5. Memorability — 15 points

- 0-5: accurate but forgettable
- 6-10: one useful phrase, distinction, image, or contrast
- 11-15: the piece leaves behind a portable idea the reader can repeat or act on

### 6. Non-genericness — 15 points

- 0-5: could have been written about almost anything
- 6-10: some original judgment, but still padded with generic transitions or interchangeable claims
- 11-15: clear human judgment, specific stakes, and wording shaped by this exact situation

## Automatic checks to run alongside the scorecard

- slop phrase count
- proof marker count
- weak opener detection
- abstract noun density
- long sentence count
- vague attribution / fake citation scan
- unsupported-importance scan: claims that something is "important," "transformative," or "a key role" without a named mechanism or consequence

## Automatic penalties

Subtract:

- 15 for fake citations, unverifiable proof, or invented specifics
- 10 for legacy/significance inflation without evidence
- 10 for generic AI phrases
- 10 for padded "future prospects" or "in conclusion" ending
- 10 for a claim that cannot be attached to a named reader, event, product, company, scene, or mechanism
- 5 for platform-mismatched formatting

## Passing bar

- 85+ publishable
- 75-84 revise
- under 75 rewrite from structure

## Reviewer prompt

Ask: "If I remove the brand/person/topic names, could this still describe almost anything?" If yes, the draft fails specificity and non-genericness even if it sounds fluent.
