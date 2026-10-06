from functools import lru_cache
from typing import List, Sequence, TypedDict

from fastapi import HTTPException, status

from app.services.chunking import DocumentChunk


class EmbeddedChunk(DocumentChunk):
    embedding: List[float]


@lru_cache(maxsize=1)
def _load_model(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(model_name)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to load the configured embedding model",
        ) from error


def embed_chunks(chunks: Sequence[DocumentChunk]) -> List[EmbeddedChunk]:
    non_empty_chunks = [chunk for chunk in chunks if chunk["content"].strip()]
    if not non_empty_chunks:
        return []

    model = _load_model(_get_embedding_model_name())
    texts = [chunk["content"] for chunk in non_empty_chunks]

    try:
        vectors = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate chunk embeddings",
        ) from error

    return [
        {
            **chunk,
            "embedding": [float(value) for value in vector.tolist()],
        }
        for chunk, vector in zip(non_empty_chunks, vectors)
    ]


def embed_query(query: str) -> List[float]:
    if not query or not query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must not be empty",
        )

    model = _load_model(_get_embedding_model_name())
    try:
        vector = model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False,
        )[0]
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate query embedding",
        ) from error

    return [float(value) for value in vector.tolist()]


def _get_embedding_model_name() -> str:
    from app.core.config import settings

    return settings.embedding_model


__all__ = ["EmbeddedChunk", "embed_chunks", "embed_query"]
