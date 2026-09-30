from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentMetadataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    title: Optional[str]
    effective_date: Optional[date]
    expiry_date: Optional[date]
    version: Optional[str]
    language: Optional[str]
