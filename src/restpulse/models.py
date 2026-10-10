from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    """Generic wrapper for validated API responses."""
    status_code: int
    data: Dict[str, Any]
    headers: Optional[Dict[str, str]] = None

class PulseData(BaseModel):
    """Example model representing structured payload output."""
    id: str
    source: str
    payload: Dict[str, Any] = Field(default_factory=dict)