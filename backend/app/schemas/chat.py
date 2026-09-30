from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    document_ids: Optional[List[int]] = None

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question must not be empty")
        return value

    @field_validator("document_ids")
    @classmethod
    def validate_document_ids(cls, value: Optional[List[int]]) -> Optional[List[int]]:
        if value is not None and any(document_id <= 0 for document_id in value):
            raise ValueError("document_ids must contain positive integers")
        return value


class ChatSource(BaseModel):
    document_id: int
    document_name: str
    page: int
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatSource]
