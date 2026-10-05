from pathlib import Path
import re
from typing import Iterator, List, Mapping, Optional, Tuple, TypedDict
import logging
import fitz
from fastapi import HTTPException, status

from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import Document, DocumentContent, DocumentStatus
from app.services.chunking import chunk_document_contents
from app.services.embeddings import EmbeddedChunk, embed_chunks
from app.services.generation import GeneratedAnswer, generate_answer, stream_answer
from app.services.retrieval import RetrievalResult, retrieve, upsert_embedded_chunks
from app.storage.files import stored_file_from_reference

logger = logging.getLogger(__name__)

INSUFFICIENT_EVIDENCE_ANSWER = (
    "I couldn't find enough information in the uploaded documents to answer this question."
)
_INSUFFICIENT_PHRASES = (
    "not enough information",
    "insufficient information",
    "cannot be determined",
    "can't be determined",
    "could not determine",
    "couldn't determine",
    "do not provide enough information",
)
_FACT_TOKEN_PATTERN = re.compile(
    r"(?<!\w)(?:\$\s*)?\d+(?:[,.]\d+)*(?:\s*%|\s*(?:days?|months?|years?))?\b",
    re.IGNORECASE,
)
_WORD_PATTERN = re.compile(r"\b[a-zA-Z]{4,}\b")
_COMMON_WORDS = {
    "about",
    "available",
    "does",
    "from",
    "have",
    "information",
    "into",
    "that",
    "than",
    "the",
    "this",
    "what",
    "when",
    "which",
    "with",
}

class ExtractedPage(TypedDict):
    document_id: int
    page_number: int
    text: str


class AnswerSource(TypedDict):
    document_id: int
    document_name: str
    page: int
    excerpt: str


def _build_answer_sources(
    retrieved_chunks: List[RetrievalResult],
) -> List[AnswerSource]:
    sources: List[AnswerSource] = []
    seen_chunk_ids = set()

    for chunk in retrieved_chunks:
        if chunk["chunk_id"] in seen_chunk_ids:
            continue
        seen_chunk_ids.add(chunk["chunk_id"])
        sources.append(
            {
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "page": chunk["page_number"],
                "excerpt": chunk["chunk_text"],
            }
        )

    return sources