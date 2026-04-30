from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_rel(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_roadmap_stops_numbered_phases_at_phase_12():
    roadmap = read_rel("ROADMAP.md")

    assert "## Phase 12 — Endgame: Writing Operating System" in roadmap
    assert "## Post-v1 Tracks" in roadmap
    assert "After Phase 12, ProseKernel is considered v1-complete." in roadmap
    for phase in range(13, 21):
        assert f"Phase {phase}" not in roadmap


def test_post_v1_tracks_have_statuses_and_priorities():
    roadmap = read_rel("ROADMAP.md")

    for track, status in [
        ("Track A — Structured Outputs / Agent API", "Planned"),
        ("Track B — CI, Release, and Package Hardening", "Mostly implemented / release hardening in progress"),
        ("Track C — Public Distribution", "In progress"),
        ("Track D — Evaluation Maturity", "Later"),
        ("Track E — Library and Pattern Scale", "Later"),
        ("Track F — Provider and Local Model Support", "Optional"),
        ("Track G — Product Surfaces", "Experimental"),
    ]:
        assert f"### {track}" in roadmap
        track_section = roadmap.split(f"### {track}", 1)[1].split("\n### ", 1)[0]
        assert f"Status: {status}" in track_section

    assert "prosekernel brief \"Write a launch email for an AI writing tool\" --json" in roadmap
    assert "Public launch should happen after:" in roadmap


def test_v1_definition_of_done_doc_is_concrete_and_bounded():
    doc = read_rel("docs/v1-definition-of-done.md")
    readme = read_rel("README.md")

    assert "# ProseKernel v1 Definition of Done" in doc
    assert "## Stop Building Rule" in doc
    assert "v1 does not require" in doc
    for non_goal in ["web UI", "MCP server", "editor plugin", "local model support", "hundreds of examples"]:
        assert non_goal in doc
    assert "docs/v1-definition-of-done.md" in readme
