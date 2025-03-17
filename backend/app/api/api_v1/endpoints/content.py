from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....schemas.content import Content, ContentCreate, ContentUpdate
from ....models.models import ContentType
from ....services.content import ContentService
from ....utils.youtube import YouTubeTranscriptExtractor
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
youtube = YouTubeTranscriptExtractor()


@router.post("/youtube", response_model=Content)
async def create_youtube_content(
    *,
    video_url: str = Body(..., embed=True),
    db: Session = Depends(get_db)
) -> Content:
    """
    Create content from YouTube video transcript.
    """
    try:
        logger.debug(f"Processing YouTube video: {video_url}")
        
        # Extract transcript and metadata
        transcript = youtube.extract_transcript(video_url)
        if not transcript:
            raise HTTPException(
                status_code=400,
                detail="Could not extract transcript from video"
            )
            
        metadata = youtube.get_video_metadata(video_url)
        if not metadata:
            raise HTTPException(
                status_code=400,
                detail="Could not extract metadata from video"
            )
        
        logger.debug(f"Successfully extracted transcript and metadata for video: {video_url}")
        
        # Convert video_url to string to avoid Pydantic URL type issues
        content_data = ContentCreate(
            title=metadata["title"],
            content_type=ContentType.YOUTUBE,
            source_url=str(video_url),
            content_text=transcript,
            content_metadata=metadata
        )
        
        return ContentService(db).create(content_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing YouTube video: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process YouTube video: {str(e)}"
        )


@router.post("/pdf", response_model=Content)
async def create_pdf_content(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Content:
    """
    Create content from PDF file.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="File must be a PDF"
        )
    
    # TODO: Implement PDF processing
    raise HTTPException(
        status_code=501,
        detail="PDF processing not implemented yet"
    )


@router.get("/", response_model=List[Content])
def list_contents(
    skip: int = 0,
    limit: int = 100,
    content_type: Optional[ContentType] = None,
    db: Session = Depends(get_db)
) -> List[Content]:
    """
    List all contents with optional filtering.
    """
    return ContentService(db).get_multi(skip=skip, limit=limit, content_type=content_type)


@router.get("/{content_id}", response_model=Content)
def get_content(
    content_id: int,
    db: Session = Depends(get_db)
) -> Content:
    """
    Get specific content by ID.
    """
    content = ContentService(db).get(content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )
    return content


@router.put("/{content_id}", response_model=Content)
def update_content(
    content_id: int,
    content_in: ContentUpdate,
    db: Session = Depends(get_db)
) -> Content:
    """
    Update content.
    """
    content = ContentService(db).get(content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )
    return ContentService(db).update(content, content_in)


@router.delete("/{content_id}")
def delete_content(
    content_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Delete content.
    """
    content = ContentService(db).get(content_id)
    if not content:
        raise HTTPException(
            status_code=404,
            detail="Content not found"
        )
    ContentService(db).remove(content_id)
    return {"message": "Content deleted successfully"} 