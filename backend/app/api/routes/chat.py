import json
from typing import Iterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import answer_question, stream_answer_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return answer_question(
        question=request.question,
        document_ids=request.document_ids,
    )


def _stream_events(request: ChatRequest) -> Iterator[str]:
    try:
        for event_name, payload in stream_answer_question(
            question=request.question,
            document_ids=request.document_ids,
        ):
            yield (
                f"event: {event_name}\n"
                f"data: {json.dumps(payload)}\n\n"
            )
    except HTTPException as error:
        yield (
            "event: error\n"
            f"data: {json.dumps({'detail': error.detail})}\n\n"
        )
    except Exception:
        yield (
            "event: error\n"
            f"data: {json.dumps({'detail': 'Unable to stream chat response'})}\n\n"
        )


@router.post("/stream")
def chat_stream(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        _stream_events(request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
