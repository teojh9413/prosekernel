# PATTERN_UX_001 — Actionable recovery microcopy

## Use when
Use this pattern for error messages, empty states, onboarding prompts, permission requests, product warnings, and transactional UI copy where the reader needs to recover or take the next useful action.

## Reader situation
The reader is not reading for pleasure. They are trying to complete a task, understand a consequence, or recover from a mistake. Their patience is low, and vague friendliness can feel like friction.

## Structure
1. State what happened in the user’s language.
2. If needed, name why it happened without blaming the user.
3. Tell the user exactly what to do next.
4. Preserve necessary constraints, consequences, or irreversible risk.
5. Remove decorative warmth unless it makes the next action clearer.

## Why it works
Good microcopy is not miniature branding. It is interface behavior expressed in language. Recovery copy works when it reduces uncertainty at the moment of friction: what happened, why it matters, and what to do now.

## Examples
- `library/ux-product-microcopy/examples/govuk-error-message.md` — writes validation messages that tell users exactly how to recover.
- `library/ux-product-microcopy/examples/shopify-polaris-actionable-language.md` — makes interface language action-oriented and consequence-aware.
- `library/ux-product-microcopy/examples/apple-hig-writing-guidance.md` — treats brevity as usability, not as a style affectation.
- `library/ux-product-microcopy/examples/mailchimp-voice-and-tone-content-guide.md` — separates stable voice from situational tone so emotion fits context.
- `library/crisis-communications/examples/slack-january-2021-outage-explanation.md` — shows how status language can layer information for different urgency levels.

## Anti-patterns
- “Oops! Something went wrong” with no recovery instruction.
- Friendly tone that hides consequences or next steps.
- Error copy written from the system’s perspective instead of the user’s task.
- Telling users to “try again” when the problem requires a specific fix.
- Packing legal, brand, and product desires into one small UI moment.

## Agent instruction
For every piece of microcopy, identify the user’s immediate job. Draft in this order: state → cause if useful → next action → consequence. Then delete any word that does not help the user decide or recover.
