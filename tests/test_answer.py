from generation.answer import NOT_FOUND, build_context, extract_citations, strip_reasoning

HITS = [
    {"source": "a.pdf", "page": 3, "text": "alpha"},
    {"source": "b.pdf", "page": 7, "text": "beta"},
]


def test_build_context_numbers_passages():
    context = build_context(HITS)
    assert "[1] (a.pdf, page 3)" in context
    assert "[2] (b.pdf, page 7)" in context


def test_extract_citations_ignores_invalid_numbers():
    assert extract_citations("Yes [2]. Also [9] and [2].", HITS) == [HITS[1]]


def test_strip_reasoning_handles_missing_opening_tag():
    assert strip_reasoning("long thoughts [1] [2]\n</think>\n\n21 days [1]") == "21 days [1]"


def test_strip_reasoning_leaves_clean_text_alone():
    assert strip_reasoning("21 days [1]") == "21 days [1]"


def test_refusal_has_no_citations():
    assert extract_citations(f"{NOT_FOUND} [1]", HITS) == []
