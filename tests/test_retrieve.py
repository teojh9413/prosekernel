from pathlib import Path

from humanprint.retrieve import load_examples, parse_frontmatter, section_text, select_examples

ROOT = Path(__file__).resolve().parents[1]


def test_load_examples_reads_current_corpus():
    examples = load_examples(ROOT)
    assert len(examples) >= 60
    assert any(example.title == "Apple iPod — 1,000 Songs in Your Pocket" for example in examples)
    assert any(example.category == "email-newsletters" for example in examples)
    assert any(example.category == "crisis-communications" for example in examples)
    assert all(example.craft_moves for example in examples)


def test_select_examples_uses_seeded_new_category_first():
    examples = select_examples(ROOT, "write a launch email for Humanprint", limit=5)
    assert examples
    assert examples[0].category == "email-newsletters"


def test_select_examples_uses_neighbors_for_sparse_new_category():
    examples = select_examples(ROOT, "write an outage apology after a product incident", limit=5)
    categories = {example.category for example in examples}
    assert examples[0].category == "crisis-communications"
    assert "technical-explanatory" in categories or "strategic-intelligent" in categories


def test_parse_frontmatter_and_sections():
    path = ROOT / "library" / "essays-literary" / "examples" / "orwell-politics-english-language.md"
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    assert frontmatter["category"] == "essays-literary"
    assert "clarity" in frontmatter["tags"]
    assert section_text(text, "Craft moves")
