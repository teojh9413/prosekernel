# ProseKernel Rewrite Report

Source draft: safe public demo draft
Task: write a launch email for an AI writing tool
Retrieval mode: hybrid

> No model call was made. This rewrite is deterministic and should be treated as a source-safe working draft, not final copy.

## Quality delta
Scorecard: 54/100 → 87/100 (+33)
Lint: 70/100 → 85/100 (+15)

## Revision plan used
- Replace abstract claims with concrete nouns, named situations, numbers, or constraints.
- Make the structure visible with a reader problem, claim, proof, tradeoff, and next action.
- Add one contrast, rule, or bottom-line sentence the reader can repeat.
- Cut sentences that could describe any other product, company, or topic.
- Replace flagged AI-slop phrases with plain, testable language.

## Rewritten draft
# Rewritten draft

Reader: you need the piece to answer the practical question before it tries to sound finished.

Problem: write a launch email for an AI writing tool fails if it opens with generic importance. The reader needs the concrete situation, the constraint, and the next action.

Claim: For this task, the draft should give the reader a clear path through write a launch email for an AI writing tool, not a polished generality.

Proof: Use the source fact as the anchor: Launch day is here and we are excited to announce our new AI writing tool. It helps teams write better content faster. In today's fast-paced world, communication is more importa...

Tradeoff: this is slower than instant polish, but it prevents the common failure mode: confident copy that could describe any product, policy, or workflow.

Next action: fix the highest-penalty line first, preserve the source facts, then publish only after the scorecard and human read-aloud pass.

Craft transfer:
- Opens with the relationship: why the reader is receiving this and what they joined.
- States the publication promise in concrete terms.

Source pattern studied: Substack — Writing a good welcome email

## Retrieved examples
- Substack — Writing a good welcome email — email-newsletters — `library/email-newsletters/examples/substack-welcome-email-guide.md`
- The Marginalian — Sunday Digest Curatorial Letter — email-newsletters — `library/email-newsletters/examples/marginalian-sunday-digest-curatorial-letter.md`
- Morning Brew daily briefing voice — email-newsletters — `library/email-newsletters/examples/morning-brew-daily-briefing-voice.md`
- GitHub Changelog — Release Note Cadence — email-newsletters — `library/email-newsletters/examples/github-changelog-release-note-cadence.md`
- James Clear 3-2-1 newsletter format — email-newsletters — `library/email-newsletters/examples/james-clear-3-2-1-newsletter-format.md`

## Patterns applied
- `PATTERN_EMAIL_001`
- `PATTERN_UX_001`
- `PATTERN_HOOK_001`
- `PATTERN_EXPLAIN_001`
- `PATTERN_SPEECH_001`

## Quality gate
- Run `prosekernel scorecard rewritten.md --task 'write a launch email for an AI writing tool'`.
- Run `prosekernel lint rewritten.md`.
- Do a human read-aloud pass for rhythm, compression, and factual proof.
