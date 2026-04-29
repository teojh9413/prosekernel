from pathlib import Path

from prosekernel.cli import main
from prosekernel.retrieve import (
    _semantic_token_tuple,
    load_examples,
    parse_frontmatter,
    rank_examples,
    section_text,
    select_examples,
    semantic_tokens,
)
from prosekernel.patterns import KNOWN_PATTERN_IDS

ROOT = Path(__file__).resolve().parents[1]


def test_load_examples_reads_current_corpus():
    examples = load_examples(ROOT)
    assert len(examples) >= 100
    assert any(example.title == "Apple iPod — 1,000 Songs in Your Pocket" for example in examples)
    assert any(example.category == "email-newsletters" for example in examples)
    assert any(example.category == "crisis-communications" for example in examples)
    assert all(example.craft_moves for example in examples)
    assert all(example.pattern_ids for example in examples)


def test_all_examples_link_to_strict_patterns():
    known = set(KNOWN_PATTERN_IDS)
    for example in load_examples(ROOT):
        assert set(example.pattern_ids) <= known
        for pattern_id in example.pattern_ids:
            assert list((ROOT / "patterns").glob(f"{pattern_id}-*.md"))

def test_select_examples_uses_seeded_new_category_first():
    examples = select_examples(ROOT, "write a launch email for ProseKernel", limit=5)
    assert examples
    assert examples[0].category == "email-newsletters"


def test_select_examples_uses_neighbors_for_sparse_new_category():
    examples = select_examples(ROOT, "write a civic speech about public duty", limit=5)
    categories = {example.category for example in examples}
    assert examples[0].category == "speeches-oratory"
    assert "essays-literary" in categories or "strategic-intelligent" in categories


def test_rank_examples_exposes_hybrid_score_breakdown():
    matches = rank_examples(
        ROOT,
        "write a customer trust update after a compromised credential scare",
        limit=5,
        mode="hybrid",
    )
    assert matches
    assert matches[0].example.category == "crisis-communications"
    assert matches[0].semantic_score > 0
    assert matches[0].hybrid_score >= matches[0].lexical_score
    assert matches[0].retrieval_mode == "hybrid"


def test_hybrid_retrieval_can_be_requested_without_changing_default_contract():
    task = "write an internal ownership note that prevents stalled decisions"
    default_examples = select_examples(ROOT, task, limit=3)
    hybrid_examples = select_examples(ROOT, task, limit=3, mode="hybrid")
    assert all(hasattr(example, "title") for example in default_examples)
    assert all(hasattr(example, "title") for example in hybrid_examples)
    assert hybrid_examples[0].category == "internal-ops-docs"


def test_semantic_token_expansion_is_offline_cached_and_copy_safe():
    _semantic_token_tuple.cache_clear()
    first = semantic_tokens("credential scare trust update")
    first.add("caller-mutation")
    second = semantic_tokens("credential scare trust update")
    info = _semantic_token_tuple.cache_info()

    assert {"security", "trust", "credential"} <= second
    assert "caller-mutation" not in second
    assert info.hits >= 1


def test_search_examples_cli_explain_shows_hybrid_breakdown(capsys):
    rc = main([
        "search-examples",
        "write a security incident update for customers",
        "--root",
        str(ROOT),
        "--limit",
        "2",
        "--mode",
        "hybrid",
        "--explain",
    ])
    captured = capsys.readouterr()
    assert rc == 0
    assert "Retrieval mode: hybrid" in captured.out
    assert "lexical=" in captured.out
    assert "semantic=" in captured.out


def test_parse_frontmatter_and_sections():
    path = ROOT / "library" / "essays-literary" / "examples" / "orwell-politics-english-language.md"
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    assert frontmatter["category"] == "essays-literary"
    assert "clarity" in frontmatter["tags"]
    assert section_text(text, "Craft moves")
