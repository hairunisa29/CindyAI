from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessageBase(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatMessageCreate(ChatMessageBase):
    chat_id: int
    content_id: Optional[int] = None
    content_metadata: Optional[Dict[str, Any]] = None


class ChatMessage(ChatMessageBase):
    id: int
    chat_id: int
    content_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    title: Optional[str] = None


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessage] = []

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    message: ChatMessage
    context: Optional[Dict[str, str]] = None
    sources: Optional[List[Dict[str, Any]]] = None 