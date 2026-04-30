# ProseKernel Writing Brief

Task: write a launch email for an AI writing tool
Retrieval mode: lexical

> Dry-run mode: No model call was made. This report is a provider-agnostic brief for any AI agent or LLM adapter.

## Recommended categories
- email-newsletters

## Retrieved examples
- The Marginalian — Sunday Digest Curatorial Letter — email-newsletters — `library/email-newsletters/examples/marginalian-sunday-digest-curatorial-letter.md`
  - Use when: When an editorial newsletter must feel like a recurring intellectual ritual rather than a list of links.
  - Patterns: PATTERN_EMAIL_001, PATTERN_HOOK_001
- Morning Brew daily briefing voice — email-newsletters — `library/email-newsletters/examples/morning-brew-daily-briefing-voice.md`
  - Use when: When summarizing serious information without making the email feel like homework.
  - Patterns: PATTERN_EMAIL_001
- Substack — Writing a good welcome email — email-newsletters — `library/email-newsletters/examples/substack-welcome-email-guide.md`
  - Use when: When writing a welcome email, newsletter onboarding note, or first-touch creator message.
  - Patterns: PATTERN_EMAIL_001, PATTERN_UX_001
- GitHub Changelog — Release Note Cadence — email-newsletters — `library/email-newsletters/examples/github-changelog-release-note-cadence.md`
  - Use when: When recurring technical updates need to stay scannable, trustworthy, and useful without editorial padding.
  - Patterns: PATTERN_EMAIL_001, PATTERN_EXPLAIN_001
- James Clear 3-2-1 newsletter format — email-newsletters — `library/email-newsletters/examples/james-clear-3-2-1-newsletter-format.md`
  - Use when: When designing a newsletter readers can recognize, skim, and keep opening.
  - Patterns: PATTERN_EMAIL_001, PATTERN_SPEECH_001

## Patterns to apply
- `PATTERN_EMAIL_001`
- `PATTERN_HOOK_001`
- `PATTERN_UX_001`
- `PATTERN_EXPLAIN_001`
- `PATTERN_SPEECH_001`

Agent instructions:
- PATTERN_EMAIL_001: For any email sequence, write the promise before the prose. Fill this sentence first: “Every [cadence], you will get [specific value] so you can [reader outcome].” Then draft the email around that promise and remove competing CTAs.
- PATTERN_HOOK_001: Before drafting the opening, ask: “What distinction would make this problem easier to see?” Name the two sides in simple language, show one consequence, then use the rest of the piece to make the distinction useful rather than merely clever.
- PATTERN_UX_001: For every piece of microcopy, identify the user’s immediate job. Draft in this order: state → cause if useful → next action → consequence. Then delete any word that does not help the user decide or recover.
- PATTERN_EXPLAIN_001: When explaining a complex topic, write the learning ladder first: task → first concept → example → next concept → edge cases. Draft only one rung at a time, and move advanced detail later unless it is required for the current step.
- PATTERN_SPEECH_001: Before drafting a speech, write the duty sentence first: “Because [shared principle] is being tested by [present moment], we must [unfinished work].” Then build the speech backward through origin, test, cost, humility, and renewed duty.

## Craft moves
- Builds trust through a stable editorial worldview.
- Frames links as part of an ongoing conversation with the reader.
- Uses recurrence to create ritual rather than urgency.
- Lets curation signal taste and values.
- Balances personal voice with service to the reader’s inner life.
- Packages multiple topics into predictable sections.
- Uses voice to reduce dryness without hiding facts.

## Agent drafting prompt
```text
You are drafting with ProseKernel, an open-source writing taste layer for AI agents.

Task: write a launch email for an AI writing tool

Operating rules:
- Do structure transfer, not phrase transfer.
- Do not copy source phrases.
- Lead with the reader's concrete situation before polish.
- Use specific proof: names, numbers, examples, mechanisms, scenes, or constraints.
- Avoid generic AI slop, fake significance, and unsupported certainty.

Retrieved examples to study:
- The Marginalian — Sunday Digest Curatorial Letter [email-newsletters] — use when: When an editorial newsletter must feel like a recurring intellectual ritual rather than a list of links.
- Morning Brew daily briefing voice [email-newsletters] — use when: When summarizing serious information without making the email feel like homework.
- Substack — Writing a good welcome email [email-newsletters] — use when: When writing a welcome email, newsletter onboarding note, or first-touch creator message.
- GitHub Changelog — Release Note Cadence [email-newsletters] — use when: When recurring technical updates need to stay scannable, trustworthy, and useful without editorial padding.
- James Clear 3-2-1 newsletter format [email-newsletters] — use when: When designing a newsletter readers can recognize, skim, and keep opening.

Patterns to apply:
- PATTERN_EMAIL_001: For any email sequence, write the promise before the prose. Fill this sentence first: “Every [cadence], you will get [specific value] so you can [reader outcome].” Then draft the email around that promise and remove competing CTAs.
- PATTERN_HOOK_001: Before drafting the opening, ask: “What distinction would make this problem easier to see?” Name the two sides in simple language, show one consequence, then use the rest of the piece to make the distinction useful rather than merely clever.
- PATTERN_UX_001: For every piece of microcopy, identify the user’s immediate job. Draft in this order: state → cause if useful → next action → consequence. Then delete any word that does not help the user decide or recover.
- PATTERN_EXPLAIN_001: When explaining a complex topic, write the learning ladder first: task → first concept → example → next concept → edge cases. Draft only one rung at a time, and move advanced detail later unless it is required for the current step.
- PATTERN_SPEECH_001: Before drafting a speech, write the duty sentence first: “Because [shared principle] is being tested by [present moment], we must [unfinished work].” Then build the speech backward through origin, test, cost, humility, and renewed duty.

Craft moves to transfer:
- Builds trust through a stable editorial worldview.
- Frames links as part of an ongoing conversation with the reader.
- Uses recurrence to create ritual rather than urgency.
- Lets curation signal taste and values.
- Balances personal voice with service to the reader’s inner life.
- Packages multiple topics into predictable sections.
- Uses voice to reduce dryness without hiding facts.

Drafting sequence:
1. Name the reader and their current moment.
2. Choose one primary pattern and make the structure visible.
3. Draft with concrete proof before claims of importance.
4. Cut any sentence that could describe any other product, company, or topic.
5. Score the draft before publishing with `prosekernel scorecard draft.md --task "..."`.
```

## Quality gate
- Run `prosekernel lint draft.md`.
- Run `prosekernel scorecard draft.md --task "write a launch email for an AI writing tool"`.
- Revise until the draft has concrete proof, reader fit, and non-genericness.
