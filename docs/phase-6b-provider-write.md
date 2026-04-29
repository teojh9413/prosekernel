# Phase 6B — Explicit Provider Write Mode

ProseKernel write mode turns the Phase 6A brief into an LLM draft, then immediately runs the ProseKernel quality gates.

The safety contract is strict:

- `prosekernel brief` remains the no-credential, no-model-call dry run.
- `prosekernel write` never chooses a provider by default.
- A write run requires both `--provider` and `--model`.
- Missing credentials fail before any API call.
- Provider calls are adapter-based so agents can inject their own local or test provider.

## Dry run first

Use this when you want an agent-ready packet without spend or credentials:

```bash
prosekernel brief "write a launch email for ProseKernel" --output /tmp/prosekernel-brief.md
```

The brief includes:

- recommended categories
- retrieved examples
- strict pattern instructions
- craft moves
- an agent drafting prompt
- lint and scorecard commands

## LLM-backed write mode

Write mode requires explicit provider and model selection:

```bash
prosekernel write "write a launch email for ProseKernel" \
  --provider openai \
  --model gpt-4o-mini \
  --output /tmp/prosekernel-write.md
```

Supported initial providers:

- `openai` using `OPENAI_API_KEY`
- `openrouter` using `OPENROUTER_API_KEY`
- `anthropic` using `ANTHROPIC_API_KEY`

You can also pass `--api-key` explicitly, but environment variables are preferred for shell history hygiene.

## No default provider

This intentionally fails:

```bash
prosekernel write "write a launch email for ProseKernel"
```

Expected behavior:

```text
No default provider is configured. ProseKernel will not choose a paid provider for you. Use `prosekernel brief` for a no-credential dry run, or pass --provider and --model explicitly.
```

## Missing credentials

This also fails safely if the provider key is absent:

```bash
prosekernel write "write a launch email for ProseKernel" --provider openai --model gpt-4o-mini
```

Expected behavior:

```text
Missing credential for provider 'openai'. Set OPENAI_API_KEY or pass --api-key explicitly. No API call was made. Use `prosekernel brief` for a no-credential dry run.
```

## Output contract

A successful write report includes:

1. task
2. explicit provider and model metadata
3. retrieved examples
4. pattern IDs used
5. craft moves transferred
6. model draft
7. anti-slop lint result
8. scorecard result
9. revision-quality gate

## Adapter contract

The engine accepts any adapter with this shape:

```python
class ProviderAdapter(Protocol):
    provider: str
    model: str

    def generate(self, prompt: str) -> str:
        ...
```

This lets coding agents, tests, or local model wrappers run ProseKernel without coupling the engine to a specific vendor SDK.

## Design principle

ProseKernel should be taste infrastructure, not a hidden spending surface. If a model call happens, the caller must have made a visible provider/model/credential choice.
