from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SupplierCreate(BaseModel):
    name: str
    contact_information: Optional[str] = None


class SupplierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    contact_information: Optional[str]
    created_at: datetime
    updated_at: datetime
