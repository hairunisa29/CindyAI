from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ....db.session import get_db
from ....schemas.chat import Chat, ChatCreate, ChatResponse
from ....services.chat import ChatService

router = APIRouter()


@router.post("", response_model=Chat)
def create_chat(
    *,
    chat_in: ChatCreate,
    db: Session = Depends(get_db)
) -> Chat:
    """
    Create new chat session.
    """
    return ChatService(db).create_chat(chat_in)


@router.get("/{chat_id}", response_model=Chat)
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db)
) -> Chat:
    """
    Get chat by ID.
    """
    chat = ChatService(db).get_chat(chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    return chat


@router.post("/{chat_id}/message", response_model=ChatResponse)
async def send_message(
    chat_id: int,
    *,
    message: str = Body(..., embed=True),
    video_id: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
) -> ChatResponse:
    """
    Send a message in a chat and get AI response.
    Optionally provide a video_id to contextualize the response to a specific video.
    """
    chat = ChatService(db).get_chat(chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
    
    response = await ChatService(db).process_message(chat_id, message, video_id)
    return ChatResponse(**response)