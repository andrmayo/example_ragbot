from resume_ragbot.rag.chunking import chunk_text, Chunk


def test_chunk_empty_text():
    chunks = chunk_text("", source="test.txt")
    assert chunks == []


def test_chunk_short_text():
    chunks = chunk_text("Short text.", source="test.txt")
    assert len(chunks) == 1
    assert chunks[0].text == "Short text."
    assert chunks[0].source == "test.txt"


def test_chunk_respects_size():
    text = "A" * 1000
    chunks = chunk_text(text, source="test.txt", chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 3
    assert all(len(c.text) <= 500 for c in chunks)


def test_chunk_overlap():
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."
    chunks = chunk_text(text, source="test.txt", chunk_size=30, chunk_overlap=10)
    assert len(chunks) > 1
