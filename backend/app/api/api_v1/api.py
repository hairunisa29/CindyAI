from fastapi import APIRouter
from .endpoints import content, chat

api_router = APIRouter()

api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"]) 