from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str  # Document identifier
    index: int  # Chunk index within document


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    """
    Split text into overlapping chunks.

    Args:
        text: The text to chunk
        source: Identifier for the source document
        chunk_size: Target size of each chunk in characters
        chunk_overlap: Number of characters to overlap between chunks
    """
    if not text.strip():
        return []

    chunks: list[Chunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size
        min_chunk_end = start + chunk_size // 2

        # If not at end, try to break at sentence or paragraph boundary
        if end < len(text):
            paragraph_break = text.rfind("\n\n", start, end)
            if paragraph_break > min_chunk_end:
                end = paragraph_break + 2
            else:
                # Look for sentence break
                for sep in (". ", ".\n", "? ", "!\n"):
                    sentence_break = text.rfind(sep, start, end)
                    if sentence_break > min_chunk_end:
                        end = sentence_break + len(sep)
                        break

        text_chunk = text[start:end].strip()
        if text_chunk:
            chunks.append(Chunk(text=text_chunk, source=source, index=index))
            index += 1

        start = end - chunk_overlap

    return chunks
