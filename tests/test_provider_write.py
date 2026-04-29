from pathlib import Path

from humanprint.cli import main
from humanprint.engine import render_provider_write_report, run_provider_write
from humanprint.providers import ProviderAdapter

ROOT = Path(__file__).resolve().parents[1]


class FakeProvider:
    provider = "fake"
    model = "fake-model"

    def __init__(self):
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return """# Launch email draft

Reader: agent builders who know their generated copy sounds over-smoothed.

Humanprint gives the agent a concrete sequence before it writes: retrieve strong examples, apply named patterns, draft from proof, then score the result for specificity and slop.

Use it when the cost of generic writing is trust: launch emails, incident notes, product explanations, and strategic memos.
"""


def test_provider_adapter_protocol_accepts_fake_provider():
    provider: ProviderAdapter = FakeProvider()

    draft = provider.generate("Draft with concrete proof.")

    assert "Humanprint" in draft


def test_run_provider_write_uses_injected_adapter_without_api_call():
    provider = FakeProvider()

    result = run_provider_write(
        ROOT,
        "write a launch email for Humanprint",
        provider_adapter=provider,
        limit=3,
    )

    assert result.provider == "fake"
    assert result.model == "fake-model"
    assert "Humanprint gives the agent" in result.draft
    assert result.brief.pattern_ids
    assert result.lint_report.score > 0
    assert result.scorecard.total > 0
    assert len(provider.prompts) == 1
    assert "Do structure transfer, not phrase transfer." in provider.prompts[0]
    assert "PATTERN_EMAIL_001" in provider.prompts[0]


def test_render_provider_write_report_includes_trace_and_quality_results():
    result = run_provider_write(
        ROOT,
        "write a launch email for Humanprint",
        provider_adapter=FakeProvider(),
        limit=3,
    )
    report = render_provider_write_report(result)

    assert "# Humanprint Write Report" in report
    assert "Provider: fake" in report
    assert "Model: fake-model" in report
    assert "## Retrieved examples" in report
    assert "PATTERN_EMAIL_001" in report
    assert "## Draft" in report
    assert "## Lint result" in report
    assert "## Scorecard" in report
    assert "No model call was made" not in report


def test_cli_write_refuses_to_choose_default_provider(capsys):
    exit_code = main([
        "write",
        "write a launch email for Humanprint",
        "--root",
        str(ROOT),
    ])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "No default provider is configured" in captured.err
    assert "humanprint brief" in captured.err
    assert "--provider" in captured.err
    assert "--model" in captured.err


def test_cli_write_missing_credentials_are_clear(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    exit_code = main([
        "write",
        "write a launch email for Humanprint",
        "--root",
        str(ROOT),
        "--provider",
        "openai",
        "--model",
        "gpt-test",
    ])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Missing credential for provider 'openai'" in captured.err
    assert "OPENAI_API_KEY" in captured.err
    assert "No API call was made" in captured.err
    assert "humanprint brief" in captured.err
