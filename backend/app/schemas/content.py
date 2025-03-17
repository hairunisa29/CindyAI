from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.models import ContentType


class ContentBase(BaseModel):
    title: str
    content_type: ContentType
    source_url: Optional[str] = None


class ContentCreate(ContentBase):
    content_text: Optional[str] = None
    content_metadata: Optional[Dict[str, Any]] = None


class ContentUpdate(ContentBase):
    title: Optional[str] = None
    content_type: Optional[ContentType] = None
    content_text: Optional[str] = None
    content_metadata: Optional[Dict[str, Any]] = None


class ContentInDB(ContentBase):
    id: int
    content_text: Optional[str]
    content_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Content(ContentInDB):
    pass 