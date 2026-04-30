from pathlib import Path

from prosekernel.cli import main
from prosekernel.paths import RootResolutionError, resolve_root

ROOT = Path(__file__).resolve().parents[1]


def test_resolve_root_works_from_repo_root(monkeypatch):
    monkeypatch.chdir(ROOT)
    monkeypatch.delenv("PROSEKERNEL_ROOT", raising=False)

    assert resolve_root() == ROOT


def test_resolve_root_uses_explicit_root(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PROSEKERNEL_ROOT", raising=False)

    assert resolve_root(ROOT) == ROOT


def test_resolve_root_uses_prosekernel_root_env(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PROSEKERNEL_ROOT", str(ROOT))

    assert resolve_root() == ROOT


def test_resolve_root_fails_cleanly_outside_repo_without_root(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PROSEKERNEL_ROOT", raising=False)

    try:
        resolve_root()
    except RootResolutionError as exc:
        message = str(exc)
    else:
        raise AssertionError("resolve_root should fail outside a ProseKernel root")

    assert "ProseKernel needs access to its repo/data root" in message
    assert "run from the repo root" in message
    assert "--root /path/to/prosekernel" in message
    assert "PROSEKERNEL_ROOT" in message


def test_cli_fails_cleanly_instead_of_empty_retrieval_when_root_is_unknown(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PROSEKERNEL_ROOT", raising=False)

    exit_code = main(["search-examples", "write a launch email", "--limit", "1"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "ProseKernel needs access to its repo/data root" in captured.err
    assert "run from the repo root" in captured.err
    assert "--root /path/to/prosekernel" in captured.err
    assert "PROSEKERNEL_ROOT" in captured.err
    assert "Recommended categories" not in captured.out
