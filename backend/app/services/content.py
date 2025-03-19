from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from ..models.models import Content, ContentType
from ..schemas.content import ContentCreate, ContentUpdate


class ContentService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, content_id: int) -> Optional[Content]:
        return self.db.query(Content).filter(Content.id == content_id).first()

    def get_by_youtube_url(self, video_url: str) -> Optional[Content]:
        """Get content by YouTube URL."""
        return self.db.query(Content).filter(
            Content.content_type == ContentType.YOUTUBE,
            Content.source_url == video_url
        ).first()
    
    def get_by_video_id(self, video_id: str) -> Optional[Content]:
        """Get content by YouTube video ID from metadata."""
        # Filter by content type first
        contents = self.db.query(Content).filter(
            Content.content_type == ContentType.YOUTUBE
        ).all()
        
        # Then manually check the metadata for the video_id
        for content in contents:
            if content.content_metadata and 'video_id' in content.content_metadata:
                if content.content_metadata['video_id'] == video_id:
                    return content
        
        return None

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        content_type: Optional[ContentType] = None
    ) -> List[Content]:
        query = self.db.query(Content)
        if content_type:
            query = query.filter(Content.content_type == content_type)
        return query.offset(skip).limit(limit).all()

    def create(self, content_in: ContentCreate) -> Content:
        content = Content(
            title=content_in.title,
            content_type=content_in.content_type,
            source_url=str(content_in.source_url) if content_in.source_url else None,
            content_text=content_in.content_text,
            content_metadata=content_in.content_metadata
        )
        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)
        return content

    def update(self, content: Content, content_in: ContentUpdate) -> Content:
        for field, value in content_in.model_dump(exclude_unset=True).items():
            setattr(content, field, value)
        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)
        return content

    def remove(self, content_id: int) -> None:
        content = self.db.query(Content).filter(Content.id == content_id).first()
        if content:
            self.db.delete(content)
            self.db.commit()