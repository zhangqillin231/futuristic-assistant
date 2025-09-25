from fastapi import APIRouter
from ..models import ChatRequest, ChatResponse
from ..database import db

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    response_text = f"Echo: {request.message}"
    db.chats.insert_one({"user_id": request.user_id, "message": request.message, "response": response_text})
    return ChatResponse(response=response_text)