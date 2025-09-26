import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo import MongoClient

# Load env variables (works locally, Vercel injects them automatically in production)
load_dotenv()

# ====== ENV CONFIG ======
API_ORIGINS = os.environ.get("API_ORIGINS", "*").split(",")
MONGO_URI = os.environ.get("MONGODB_URI")
JWT_SECRET = os.environ.get("JWT_SECRET", "changeme")

# ====== DB Connection ======
client = MongoClient(MONGO_URI) if MONGO_URI else None
db = client.get_database("futuristic_assistant") if client else None

# ====== FastAPI app ======
app = FastAPI(title="Futuristic Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Health Check ======
@app.get("/health")
def health_check():
    return {"status": "ok", "db": bool(db)}

# ====== Example Chat ======
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # (Later: connect to OpenAI or vector store)
    return ChatResponse(reply=f"I heard: {req.message}")

# ====== WebSocket Echo ======
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass

# ====== Local Run ======
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
