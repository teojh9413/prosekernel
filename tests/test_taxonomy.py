from prosekernel.taxonomy import (
    CATEGORIES,
    BLENDED_FORMATS,
    expand_with_neighbors,
    is_known_category,
    recommend_categories,
)


def test_expanded_categories_are_known():
    for category in [
        "email-newsletters",
        "speeches-oratory",
        "journalism-reportage",
        "ux-product-microcopy",
        "crisis-communications",
        "internal-ops-docs",
    ]:
        assert category in CATEGORIES
        assert is_known_category(category)


def test_recommend_email_newsletter_category():
    assert recommend_categories("write a launch email and newsletter for ProseKernel")[0] == "email-newsletters"


def test_blended_formats_stay_mapped_not_flattened():
    assert BLENDED_FORMATS["fundraising-investor-grants"] == (
        "strategic-intelligent",
        "persuasive-copywriting",
    )


def test_neighbor_expansion_falls_back_to_populated_categories():
    expanded = expand_with_neighbors(["email-newsletters"])
    assert expanded[:2] == ("email-newsletters", "persuasive-copywriting")
    assert "essays-literary" in expanded
