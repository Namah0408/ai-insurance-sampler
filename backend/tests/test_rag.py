from app.rag.text_chunker import chunk_text


def test_chunk_text():

    text = (
        "This is a synthetic knowledge document. "
        "It contains information about sampling, "
        "identity verification and financial analysis."
    )

    chunks = chunk_text(
        text,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(chunks) > 1


def test_chunk_indexes():

    text = "A" * 200

    chunks = chunk_text(
        text,
        chunk_size=80,
        chunk_overlap=10,
    )

    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_empty_text():

    chunks = chunk_text("")

    assert chunks == []