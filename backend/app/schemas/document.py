from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.db.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    supplier_id: int
    filename: str
    document_type: str
    file_path: str
    file_size: Optional[int]
    mime_type: Optional[str]
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime
