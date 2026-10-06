from functools import lru_cache
from typing import Iterator, List, Mapping, Sequence, TypedDict

from fastapi import HTTPException, status

from app.core.config import settings


class RetrievedChunk(TypedDict):
    chunk_text: str
    document_id: int
    document_name: str
    page_number: int
    section: str
    chunk_id: str
    distance: float


class GeneratedAnswer(TypedDict):
    answer: str
    sources: List[Mapping[str, object]]


_REQUIRED_CHUNK_FIELDS = (
    "chunk_text",
    "document_id",
    "document_name",
    "page_number",
    "section",
    "chunk_id",
)

_SYSTEM_PROMPT = """Answer the question using only the supplied retrieved evidence.
Do not invent procurement terms, prices, dates, clauses, or conditions, and do not use outside knowledge or assumptions.
Preserve important numbers, prices, dates, percentages, quantities, payment terms, delivery conditions, and contractual conditions exactly or materially.
Identify the source metadata supporting the answer. Distinguish information from different documents.
If evidence conflicts, report each conflicting value with its document and page source; do not silently choose one.
If the evidence is insufficient, clearly state that the available documents do not provide enough information to answer.
"""


@lru_cache(maxsize=4)
def _get_client(base_url: str, api_key: str):
    if not base_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM_BASE_URL is not configured",
        )
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM_API_KEY is not configured",
        )

    try:
        from openai import OpenAI

        return OpenAI(base_url=base_url, api_key=api_key)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to initialize the configured LLM client",
        ) from error


def _build_context(retrieved_chunks: Sequence[Mapping[str, object]]) -> str:
    context_parts: List[str] = []
    for index, chunk in enumerate(retrieved_chunks, start=1):
        if any(field not in chunk for field in _REQUIRED_CHUNK_FIELDS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Retrieved chunk metadata is incomplete",
            )
        context_parts.append(
            "\n".join(
                [
                    f"Source {index}",
                    f"Document: {chunk['document_name']}",
                    f"Document ID: {chunk['document_id']}",
                    f"Page: {chunk['page_number']}",
                    f"Section: {chunk['section']}",
                    f"Chunk ID: {chunk['chunk_id']}",
                    f"Content:\n{chunk['chunk_text']}",
                ]
            )
        )
    return "\n\n".join(context_parts)


def generate_answer(
    question: str,
    retrieved_chunks: Sequence[Mapping[str, object]],
) -> GeneratedAnswer:
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must not be empty",
        )
    if not settings.llm_model:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM_MODEL is not configured",
        )

    context = _build_context(retrieved_chunks)
    try:
        client = _get_client(settings.llm_base_url, settings.llm_api_key)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to initialize the configured LLM client",
        ) from error

    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=_build_messages(question, context),
        )
        answer = response.choices[0].message.content
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to generate an answer from the configured LLM",
        ) from error

    if not answer or not answer.strip():
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The configured LLM returned an empty answer",
        )

    return {"answer": answer, "sources": list(retrieved_chunks)}


def _build_messages(question: str, context: str) -> List[Mapping[str, str]]:
    return [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Question: {question}\n\nRetrieved evidence:\n{context}",
        },
    ]


def stream_answer(
    question: str,
    retrieved_chunks: Sequence[Mapping[str, object]],
) -> Iterator[str]:
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must not be empty",
        )
    if not settings.llm_model:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM_MODEL is not configured",
        )

    context = _build_context(retrieved_chunks)
    try:
        client = _get_client(settings.llm_base_url, settings.llm_api_key)
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=_build_messages(question, context),
            stream=True,
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to stream an answer from the configured LLM",
        ) from error


__all__ = ["GeneratedAnswer", "RetrievedChunk", "generate_answer", "stream_answer"]
