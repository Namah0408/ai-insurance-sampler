from dataclasses import dataclass

from app.core.config import settings


@dataclass
class TextChunk:
    text: str
    chunk_index: int
    start_character: int
    end_character: int


def clean_text(text: str) -> str:

    lines = []

    for line in text.splitlines():

        cleaned = " ".join(line.split())

        if cleaned:
            lines.append(cleaned)

    return "\n".join(lines)


def chunk_text(
    text: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[TextChunk]:

    text = clean_text(text)

    if not text:
        return []

    chunk_size = (
        chunk_size
        if chunk_size is not None
        else settings.rag_chunk_size
    )

    chunk_overlap = (
        chunk_overlap
        if chunk_overlap is not None
        else settings.rag_chunk_overlap
    )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text),
        )

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                TextChunk(
                    text=chunk.strip(),
                    chunk_index=chunk_index,
                    start_character=start,
                    end_character=end,
                )
            )

        if end >= len(text):
            break

        start = end - chunk_overlap
        chunk_index += 1

    return chunks