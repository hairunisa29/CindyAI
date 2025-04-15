from fastapi import APIRouter, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.api.openai import OpenAIConnector

router = APIRouter(prefix="/chat", tags=["chat"])

async def get_openai_connector():
    return OpenAIConnector()

@router.post("/", response_model=ChatResponse)
async def generate_chat_response(
    request: ChatRequest,
    openai_connector: OpenAIConnector = Depends(get_openai_connector),
):
    response = await openai_connector.get_response(
        prompt=request.message,
        system_prompt=request.system_prompt,
    )
    return ChatResponse(response=response)
