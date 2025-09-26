import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo import MongoClient

from .actions import execute_action, ActionRequest
from .auth import verify_token

# Load env
load_dotenv()

API_ORIGINS = os.environ.get("API_ORIGINS", "*").split(",") if os.environ.get("API_ORIGINS") else ["*"]

app = FastAPI(title="2050 Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# ✅ MongoDB Setup
# =======================
MONGO_URI = os.environ.get("MONGODB_URI")
mongo_client = MongoClient(MONGO_URI) if MONGO_URI else None
db = mongo_client.get_database("assistant_db") if mongo_client else None
messages_col = db["messages"] if db else None


# =======================
# Models
# =======================
class ChatRequest(BaseModel):
    message: str
    device_id: str | None = None
    user_id: str | None = None


class ChatResponse(BaseModel):
    reply: str


# =======================
# Endpoints
# =======================
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    prompt = req.message
    response_text = f"[LLM placeholder] I heard: {prompt}"

    # ✅ Save message to MongoDB
    if messages_col:
        messages_col.insert_one({
            "user_id": req.user_id,
            "device_id": req.device_id,
            "message": prompt,
            "reply": response_text
        })

    return ChatResponse(reply=response_text)


# =======================
# Action Endpoint
# =======================
@app.post("/action")
async def action_endpoint(req: ActionRequest, token_payload: dict = Depends(verify_token)):
    res = execute_action(req, token_payload=token_payload)
    return res


# =======================
# WebSockets (bridge + audio)
# =======================
@app.websocket("/ws/audio")
async def websocket_audio(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"ACK: {data[:200]}")
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/bridge")
async def websocket_bridge(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text("pong")
    except WebSocketDisconnect:
        pass


# =======================
# Entry Point
# =======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
