# Humanprint

**AI writing that leaves fingerprints. No AI slop.**

Humanprint is a private writing system for turning AI from a generic text generator into a disciplined writer/editor. It combines:

- **CLEAR**: Cut, Lead, Eliminate dead language, Active voice, Read aloud.
- **Specificity over vibes**: proof, numbers, named details, concrete nouns.
- **Human stakes**: what the reader feels, wants, fears, or risks.
- **Persuasion fit**: match message to awareness stage, goal, and medium.
- **Rewrite discipline**: draft fast, then cut hard.

This repo is designed to become the operating system for all AI-assisted writing: prompts, checklists, templates, evaluators, and eventually model/tool integrations.

## Why this exists

Most AI writing fails because it sounds competent but empty:

- bland openings
- fake authority
- generic claims
- symmetrical lists
- hedged conclusions
- overused phrases like "unlock", "leverage", "game-changer", "in today's fast-paced world"
- no taste, no tension, no proof

Humanprint fights that by forcing every piece through a writing gauntlet.

## Quick start

```bash
python -m pip install -e .
humanprint lint path/to/draft.md
```

Example:

```bash
humanprint lint examples/ai-slop-sample.md
```

## Repo structure

```text
humanprint/
├── docs/                         # Writing doctrine and operating rules
├── prompts/                      # Writer/editor system prompts
├── templates/                    # Briefs and reusable writing forms
├── src/humanprint/               # CLI + writing linter
├── tests/                        # Regression tests for the linter
└── examples/                     # Sample slop and improved drafts
```

## Current MVP

- `humanprint lint <file>` scores a draft for common AI-slop markers.
- Prompt pack for writer + editor agents.
- Writing brief template to force intent, reader, proof, and voice before drafting.
- Anti-slop checklist based on the writing wiki.

## The standard

A draft is not done until it passes these tests:

1. **Point-first**: the reader knows the point in the first 1-2 sentences.
2. **Concrete**: claims are backed by examples, proof, or sensory detail.
3. **Human**: it sounds like someone with skin in the game wrote it.
4. **Cut**: at least 15-20% of the first draft is removed.
5. **Alive**: every paragraph has a job: hook, clarify, prove, move, or close.

## Source doctrine

This repo starts from the existing writing research in the LLM Wiki:

- Orwell: cut dead language, prefer active voice, avoid stale phrases.
- Paul Graham: writing is rewriting; sound reveals thought.
- Zinsser: strip every sentence to its cleanest components.
- Ogilvy: research beats cleverness; facts beat superlatives.
- Schwartz: persuasion depends on reader awareness stage.
- Halbert: write to a starving crowd; translate features into outcomes.
