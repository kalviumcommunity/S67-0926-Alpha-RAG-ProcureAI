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
# Numbers that come from citations / list formatting, not from document facts.
_CITATION_REF_PATTERN = re.compile(
    r"\b(?:sources?|documents?|doc|pages?|chunks?|section|id)\b\.?\s*(?:id\s*)?[:#]?\s*\d+(?:\s*[-,]\s*\d+)*",
    re.IGNORECASE,
)
_BRACKET_REF_PATTERN = re.compile(r"\[\s*\d+(?:\s*[,-]\s*\d+)*\s*\]")
_LIST_MARKER_PATTERN = re.compile(r"(?m)^\s*\d+[.)]\s+")
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

MAX_DISPLAYED_SOURCES = 3


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
    seen = set()

    for chunk in retrieved_chunks:
        key = (chunk["document_id"], " ".join(chunk["chunk_text"].split()))
        if key in seen:
            continue
        seen.add(key)
        if len(sources) >= MAX_DISPLAYED_SOURCES:
            break
        sources.append(
            {
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "page": chunk["page_number"],
                "excerpt": chunk["chunk_text"],
            }
        )

    return sources

def _number_core(token: str) -> str:
    """Compare numbers regardless of units or spacing ('12 months' == '12-month' == '12')."""
    return re.sub(r"[^\d.,]", "", token).strip(".,")


def _strip_citation_noise(answer: str, retrieved_chunks: List[RetrievalResult]) -> str:
    cleaned = answer
    for chunk in retrieved_chunks:
        for value in (chunk["chunk_id"], chunk["document_name"]):
            if value:
                cleaned = cleaned.replace(str(value), " ")
    cleaned = _CITATION_REF_PATTERN.sub(" ", cleaned)
    cleaned = _BRACKET_REF_PATTERN.sub(" ", cleaned)
    cleaned = _LIST_MARKER_PATTERN.sub("", cleaned)
    return cleaned


def _answer_is_grounded(
    answer: str,
    retrieved_chunks: List[RetrievalResult],
) -> bool:
    normalized_answer = answer.strip().lower()
    if not normalized_answer:
        return False
    if any(phrase in normalized_answer for phrase in _INSUFFICIENT_PHRASES):
        return True

    evidence = " ".join(chunk["chunk_text"] for chunk in retrieved_chunks)
    evidence_facts = {
        _number_core(token) for token in _FACT_TOKEN_PATTERN.findall(evidence)
    }
    # Metadata numbers the model is told to cite are legitimate, too.
    for chunk in retrieved_chunks:
        evidence_facts.add(str(chunk["page_number"]))
        evidence_facts.add(str(chunk["document_id"]))

    claim_text = _strip_citation_noise(answer, retrieved_chunks)
    answer_facts = {
        _number_core(token) for token in _FACT_TOKEN_PATTERN.findall(claim_text)
    }
    unsupported = answer_facts - evidence_facts
    if unsupported:
        logger.warning("Grounding check failed: unsupported numbers %s", sorted(unsupported))
        return False

    answer_words = {
        word.lower() for word in _WORD_PATTERN.findall(claim_text)
    } - _COMMON_WORDS
    evidence_words = {
        word.lower() for word in _WORD_PATTERN.findall(evidence)
    } - _COMMON_WORDS
    if not (answer_words & evidence_words):
        logger.warning("Grounding check failed: no shared words with evidence")
        return False
    return True


def _mark_failed(document_id: int) -> None:
    failure_db = SessionLocal()
    try:
        failed_document = failure_db.get(Document, document_id)
        if failed_document is not None:
            failed_document.status = DocumentStatus.FAILED
            failure_db.commit()
    except Exception:
        failure_db.rollback()
        logger.exception("Unable to persist failed status for document %s", document_id)
    finally:
        failure_db.close()

def _raise_processing_error(document_id: int, error: Exception) -> None:
    _mark_failed(document_id)
    if isinstance(error, HTTPException):
        raise error
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unable to process document {document_id}",
    ) from error

def process_document(document_id: int) -> List[EmbeddedChunk]:
    db = SessionLocal()
    processing_started = False

    try:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document {document_id} not found",
            )

        if document.status not in (
            DocumentStatus.UPLOADED,
            DocumentStatus.FAILED,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Document {document_id} cannot enter processing from "
                    f"status '{document.status.value}'"
                ),
            )

        document.status = DocumentStatus.PROCESSING
        db.commit()
        processing_started = True

        stored_file = stored_file_from_reference(
            document.file_path,
            settings.upload_directory,
        )
        if not stored_file.absolute_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stored file for document {document_id} not found",
            )

        if Path(document.file_path).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Document {document_id} is not a PDF",
            )

        try:
            with fitz.open(stored_file.absolute_path) as pdf_document:
                pages = [
                    {
                        "document_id": document_id,
                        "page_number": page_number,
                        "text": page.get_text(),
                    }
                    for page_number, page in enumerate(pdf_document, start=1)
                ]
        except (fitz.FileDataError, RuntimeError) as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to read PDF for document {document_id}",
            ) from error

        db.query(DocumentContent).filter(
            DocumentContent.document_id == document_id
        ).delete(synchronize_session=False)
        content_records = [
            DocumentContent(
                document=document,
                document_id=page["document_id"],
                content=page["text"],
                page_number=page["page_number"],
                section=None,
            )
            for page in pages
        ]
        db.add_all(content_records)
        db.flush()

        chunks = chunk_document_contents(content_records)
        embedded_chunks = embed_chunks(chunks)
        upsert_embedded_chunks(embedded_chunks)

        document.status = DocumentStatus.PROCESSED
        db.commit()
        return embedded_chunks
    except Exception as error:
        db.rollback()
        if processing_started:
            _raise_processing_error(document_id, error)
        raise

def answer_question(
    question: str,
    document_ids: Optional[List[int]] = None,
) -> GeneratedAnswer:
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must not be empty",
        )

    retrieved_chunks: List[RetrievalResult] = retrieve(
        question,
        document_ids=document_ids,
    )
    if not retrieved_chunks:
        return {
            "answer": INSUFFICIENT_EVIDENCE_ANSWER,
            "sources": [],
        }

    generated = generate_answer(question, retrieved_chunks)
    if any(
        phrase in generated["answer"].strip().lower()
        for phrase in _INSUFFICIENT_PHRASES
    ):
        return {
            "answer": INSUFFICIENT_EVIDENCE_ANSWER,
            "sources": [],
        }
    if not _answer_is_grounded(generated["answer"], retrieved_chunks):
        return {
            "answer": INSUFFICIENT_EVIDENCE_ANSWER,
            "sources": [],
        }

    return {
        "answer": generated["answer"],
        "sources": _build_answer_sources(retrieved_chunks),
    }


def stream_answer_question(
    question: str,
    document_ids: Optional[List[int]] = None,
) -> Iterator[Tuple[str, Mapping[str, object]]]:
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must not be empty",
        )

    retrieved_chunks: List[RetrievalResult] = retrieve(
        question,
        document_ids=document_ids,
    )
    if not retrieved_chunks:
        yield "chunk", {"content": INSUFFICIENT_EVIDENCE_ANSWER}
        yield "sources", {"sources": []}
        yield "done", {}
        return

    answer_parts: List[str] = []
    for token in stream_answer(question, retrieved_chunks):
        answer_parts.append(token)
        yield "chunk", {"content": token}

    generated_answer = "".join(answer_parts)
    if any(
        phrase in generated_answer.strip().lower()
        for phrase in _INSUFFICIENT_PHRASES
    ) or not _answer_is_grounded(generated_answer, retrieved_chunks):
        yield "error", {"detail": INSUFFICIENT_EVIDENCE_ANSWER}
        return

    yield "sources", {"sources": _build_answer_sources(retrieved_chunks)}
    yield "done", {}