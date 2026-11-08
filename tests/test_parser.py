from ingest.parser import clean_text


def test_clean_text_removes_blank_lines():
    assert clean_text("a\n\n  b  \n") == "a\nb"


def test_clean_text_normalizes_arabic_presentation_forms():
    assert clean_text("\ufedf") == "\u0644"  # presentation form of lam -> standard lam
