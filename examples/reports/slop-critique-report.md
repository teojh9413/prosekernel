# ProseKernel Critique Report

Draft: safe public demo draft
Task: write a launch email for an AI writing tool
Retrieval mode: hybrid

> No model call was made. This critique uses deterministic ProseKernel lint, scorecard, retrieval, and pattern guidance.

## Verdict
Status: REVISE
Scorecard: 54/100
Lint: 70/100

## Scorecard
- Specificity: 11/20 — 6 concrete markers, 1 abstract noun hits.
- Proof: 13/20 — 1 proof markers found.
- Structure: 7/15 — 1 paragraph(s), 0 long sentence(s), no weak opener.
- Reader fit: 10/15 — Reader markers plus task overlap 6.
- Memorability: 5/15 — 0 contrast/rule/memory marker(s).
- Non-genericness: 8/15 — Task overlap 6; slop phrases 2; smart-empty=False.

## Lint findings
- [ERROR] slop_phrase:1: Banned AI-slop phrase: 'in today's fast-paced world'. Replace with concrete language.
- [ERROR] slop_phrase:1: Banned AI-slop phrase: 'unlock'. Replace with concrete language.

## Revision plan
- Replace abstract claims with concrete nouns, named situations, numbers, or constraints.
- Make the structure visible with a reader problem, claim, proof, tradeoff, and next action.
- Add one contrast, rule, or bottom-line sentence the reader can repeat.
- Cut sentences that could describe any other product, company, or topic.
- Replace flagged AI-slop phrases with plain, testable language.

## Retrieved examples
- Substack — Writing a good welcome email — email-newsletters — `library/email-newsletters/examples/substack-welcome-email-guide.md`
  - Use when: When writing a welcome email, newsletter onboarding note, or first-touch creator message.
- The Marginalian — Sunday Digest Curatorial Letter — email-newsletters — `library/email-newsletters/examples/marginalian-sunday-digest-curatorial-letter.md`
  - Use when: When an editorial newsletter must feel like a recurring intellectual ritual rather than a list of links.
- Morning Brew daily briefing voice — email-newsletters — `library/email-newsletters/examples/morning-brew-daily-briefing-voice.md`
  - Use when: When summarizing serious information without making the email feel like homework.
- GitHub Changelog — Release Note Cadence — email-newsletters — `library/email-newsletters/examples/github-changelog-release-note-cadence.md`
  - Use when: When recurring technical updates need to stay scannable, trustworthy, and useful without editorial padding.
- James Clear 3-2-1 newsletter format — email-newsletters — `library/email-newsletters/examples/james-clear-3-2-1-newsletter-format.md`
  - Use when: When designing a newsletter readers can recognize, skim, and keep opening.

## Patterns to apply
- `PATTERN_EMAIL_001`
- `PATTERN_UX_001`
- `PATTERN_HOOK_001`
- `PATTERN_EXPLAIN_001`
- `PATTERN_SPEECH_001`

Craft moves:
- Opens with the relationship: why the reader is receiving this and what they joined.
- States the publication promise in concrete terms.
- Sets cadence and expectations so the reader feels oriented.
- Gives one low-friction next action instead of a menu of asks.
- Sounds like a person inviting a reader into a habit, not a brand blasting a list.

## Next command
`prosekernel rewrite safe-public-demo-draft.md --task 'write a launch email for an AI writing tool' --output rewrite.md`
