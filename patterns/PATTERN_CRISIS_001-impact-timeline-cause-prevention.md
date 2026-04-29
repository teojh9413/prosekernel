# PATTERN_CRISIS_001 — Impact, timeline, cause, prevention

## Use when
Use this pattern for outage updates, public apologies, incident reports, recalls, trust-repair notes, and postmortems where the reader needs truth before reassurance.

## Reader situation
The reader may be angry, blocked, embarrassed, or worried. They do not want brand warmth first. They want to know what happened, whether they were affected, what caused it, what is being done, and whether the organization is taking responsibility.

## Structure
1. State the incident and current status plainly.
2. Name impact: who was affected, how, and for how long.
3. Give a timeline of material events, not internal drama.
4. Explain root cause at the highest useful level of technical detail.
5. State remediation already completed.
6. State prevention work and ownership.
7. Close with accountability, not self-praise.

## Why it works
Crisis writing fails when it tries to preserve image before restoring clarity. This pattern earns trust by making the organization inspectable. The timeline separates facts from excuses; prevention turns apology into operational change.

## Examples
- `library/crisis-communications/examples/gitlab-database-outage-postmortem.md` — uses incident structure to make failure and recovery legible.
- `library/crisis-communications/examples/cloudflare-june-2022-outage-postmortem.md` — separates impact, cause, and prevention for different reader depths.
- `library/crisis-communications/examples/slack-january-2021-outage-explanation.md` — explains the incident in layers so readers can stop at the detail level they need.
- `library/technical-explanatory/examples/kubernetes-concepts-documentation-layered-model.md` — shows how layered explanation can make complex systems understandable.
- `library/ux-product-microcopy/examples/govuk-error-message.md` — demonstrates recovery-oriented language at micro scale.

## Anti-patterns
- “We take this very seriously” before saying what happened.
- Apologizing for feelings instead of impact.
- Giving a vague “technical issue” with no cause or owner.
- Burying user impact under internal chronology.
- Promising prevention without naming the mechanism or accountable work.

## Agent instruction
Draft crisis communication in this order: impact → timeline → cause → remediation → prevention. Do not add empathy language until the factual spine is clear. Remove any sentence that protects the organization’s image more than it helps the affected reader.
