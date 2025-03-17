from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship
import enum
from .base import Base
from datetime import datetime


class ContentType(str, enum.Enum):
    YOUTUBE = "youtube"
    ARTICLE = "article"
    PDF = "pdf"


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="chat")


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content_type = Column(Enum(ContentType))  # Use Enum type properly
    source_url = Column(String, nullable=True)  # Ensure it's stored as String
    content_text = Column(Text)
    content_metadata = Column(JSON, nullable=True)  # Change back to content_metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat_messages = relationship("ChatMessage", back_populates="related_content")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    role = Column(String)  # user or assistant
    content = Column(Text)
    content_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
    related_content = relationship("Content", back_populates="chat_messages") 