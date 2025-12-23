from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    summary: str
    tokens_used: int
    cost_usd: float
    audio_filename: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
