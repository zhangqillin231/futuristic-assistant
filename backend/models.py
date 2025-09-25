from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

class TrainRequest(BaseModel):
    user_id: str
    command: str
    response: str