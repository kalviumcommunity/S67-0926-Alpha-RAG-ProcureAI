from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, TypedDict

from fastapi import HTTPException, status

from app.core.config import settings
from app.services.embeddings import EmbeddedChunk, embed_query


COLLECTION_NAME = "procureai_document_chunks"


class RetrievalResult(TypedDict):
    chunk_text: str
    document_id: int
    document_name: str
    page_number: int
    section: Optional[str]
    chunk_id: str
    distance: float


@lru_cache(maxsize=1)
def _get_client():
    try:
        import chromadb

        vector_db_path = Path(settings.vector_db_path)
        vector_db_path.mkdir(parents=True, exist_ok=True)
        return chromadb.PersistentClient(path=str(vector_db_path))
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to initialize the ChromaDB vector store",
        ) from error


@lru_cache(maxsize=1)
def get_collection():
    try:
        return _get_client().get_or_create_collection(name=COLLECTION_NAME)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to initialize the ChromaDB collection",
        ) from error


def upsert_embedded_chunks(chunks: Sequence[EmbeddedChunk]) -> None:
    if not chunks:
        return

    ids: List[str] = []
    embeddings: List[List[float]] = []
    documents: List[str] = []
    metadatas: List[Dict[str, Any]] = []

    for chunk in chunks:
        chunk_id = chunk["chunk_id"]
        if not chunk_id:
            raise ValueError("Every embedded chunk must have a stable chunk_id")

        ids.append(chunk_id)
        embeddings.append(chunk["embedding"])
        documents.append(chunk["content"])
        metadatas.append(
            {
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "section": chunk["section"] or "",
                "chunk_id": chunk_id,
            }
        )

    try:
        get_collection().upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store embedded document chunks",
        ) from error


def get_chunk(chunk_id: str) -> Optional[Dict[str, Any]]:
    try:
        result = get_collection().get(ids=[chunk_id], include=["documents", "metadatas", "embeddings"])
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve the stored document chunk",
        ) from error

    if not result["ids"]:
        return None

    return {
        "id": result["ids"][0],
        "document": result["documents"][0],
        "embedding": result["embeddings"][0],
        "metadata": result["metadatas"][0],
    }


def retrieve(
    query: str,
    top_k: int = 5,
    document_ids: Optional[List[int]] = None,
) -> List[RetrievalResult]:
    if not query or not query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query must not be empty",
        )
    if top_k <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="top_k must be greater than zero",
        )

    try:
        query_embedding = embed_query(query)
        collection = get_collection()
        if collection.count() == 0:
            return []
        where = None
        if document_ids:
            where = (
                {"document_id": document_ids[0]}
                if len(document_ids) == 1
                else {"document_id": {"$in": document_ids}}
            )
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
            where=where,
        )
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve document chunks from ChromaDB",
        ) from error

    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    results: List[RetrievalResult] = []
    for chunk_id, chunk_text, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        if not metadata or any(
            key not in metadata
            for key in ("document_id", "document_name", "page_number", "section", "chunk_id")
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Stored chunk metadata is incomplete",
            )
        results.append(
            {
                "chunk_text": chunk_text,
                "document_id": metadata["document_id"],
                "document_name": metadata["document_name"],
                "page_number": metadata["page_number"],
                "section": metadata["section"],
                "chunk_id": metadata["chunk_id"] or chunk_id,
                "distance": distance,
            }
        )

    return results


__all__ = [
    "COLLECTION_NAME",
    "RetrievalResult",
    "get_chunk",
    "get_collection",
    "retrieve",
    "upsert_embedded_chunks",
]
