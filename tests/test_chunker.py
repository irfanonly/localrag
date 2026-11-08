from ingest.chunker import chunk_pages, split_text
from ingest.parser import Page

LINES = "\n".join(f"line number {i}" for i in range(200))


def test_short_text_is_one_chunk():
    assert split_text("hello\nworld", 100, 20) == ["hello\nworld"]


def test_long_text_is_split_within_size_limit():
    chunks = split_text(LINES, 200, 40)
    assert len(chunks) > 1
    assert all(len(chunk) <= 200 for chunk in chunks)


def test_consecutive_chunks_overlap():
    chunks = split_text(LINES, 200, 40)
    last_line = chunks[0].splitlines()[-1]
    assert last_line in chunks[1].splitlines()


def test_overlap_must_be_smaller_than_chunk_size():
    import pytest

    with pytest.raises(ValueError):
        split_text("text", 100, 100)


def test_chunk_pages_keeps_metadata_and_skips_blank_pages():
    pages = [
        Page("a.pdf", 1, "cover"),
        Page("a.pdf", 2, "\n".join(["some real text here"] * 5)),
    ]
    chunks = chunk_pages(pages)
    assert len(chunks) == 1
    assert chunks[0].page == 2
    assert chunks[0].chunk_id == "a.pdf:p2:c0"
