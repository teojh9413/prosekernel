from pathlib import Path

from prosekernel.cli import main

ROOT = Path(__file__).resolve().parents[1]
TRACKED_TEXT_SKIP_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
}
TRACKED_TEXT_SKIP_SUFFIXES = (".egg-info",)
BANNED_OLD_BRAND_TOKENS = (
    "Human" + "print",
    "human" + "print",
    "src/" + "human" + "print",
)


def _is_scanned_text_path(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    parts = set(relative.parts)
    if parts & TRACKED_TEXT_SKIP_PARTS:
        return False
    if any(part.endswith(TRACKED_TEXT_SKIP_SUFFIXES) for part in relative.parts):
        return False
    try:
        path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return True


def test_tracked_text_files_do_not_contain_old_brand():
    import subprocess

    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    offenders: list[str] = []
    for raw in result.stdout.splitlines():
        path = ROOT / raw
        if not path.is_file() or not _is_scanned_text_path(path):
            continue
        text = path.read_text(encoding="utf-8")
        for token in BANNED_OLD_BRAND_TOKENS:
            if token in text:
                offenders.append(f"{raw}: contains old brand token")
                break

    assert offenders == []
