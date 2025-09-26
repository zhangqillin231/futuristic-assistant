# backend/main.py
import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from .actions import execute_action, ActionRequest
from .auth import verify_token

load_dotenv()

API_ORIGINS = os.environ.get('API_ORIGINS', '*').split(',') if os.environ.get('API_ORIGINS') else ['*']

app = FastAPI(title='2050 Assistant Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Bridge clients: device_id -> websocket
BRIDGE_CLIENTS = {}

# helper to send to device
async def send_to_device(device_id: str, payload: dict):
    ws = BRIDGE_CLIENTS.get(device_id)
    if not ws:
        return False
    try:
        await ws.send_json(payload)
        return True
    except Exception:
        return False


# Try importing RAG tools (vector store). Optional
try:
    from .vector_store import VectorStore
    from .train_pipeline import model as EMB_MODEL
    VS_AVAILABLE = True
except Exception:
    VS_AVAILABLE = False


# Models
class ChatRequest(BaseModel):
    message: str
    device_id: str | None = None
    user_id: str | None = None

class ChatResponse(BaseModel):
    reply: str


# --- Routes ---
@app.post('/chat', response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    prompt = req.message
    if VS_AVAILABLE:
        try:
            q_emb = EMB_MODEL.encode([prompt], convert_to_numpy=True)[0].tolist()
            vs = VectorStore(dim=EMB_MODEL.get_sentence_embedding_dimension())
            results = vs.search(q_emb, top_k=4)
            context = '\n\n'.join(
                [r['metadata'].get('source', '') + ' - ' + str(r['metadata'].get('chunk_index', '')) for r in results]
            )
            response_text = f"[RAG placeholder] Retrieved context:\n{context}\n\nAnswer (LLM required): I heard: {prompt}"
            return ChatResponse(reply=response_text)
        except Exception as e:
            response_text = f"[LLM placeholder] I heard: {prompt} (RAG error: {str(e)})"
            return ChatResponse(reply=response_text)
    return ChatResponse(reply=f"[LLM placeholder] I heard: {prompt}")


@app.post('/action')
async def action_endpoint(req: ActionRequest, token_payload: dict = Depends(verify_token)):
    res = execute_action(req, token_payload=token_payload)
    try:
        if res.get('ok') and req.device_id:
            import asyncio
            asyncio.create_task(send_to_device(req.device_id, {
                'type': 'execute',
                'action': req.name,
                'params': req.params
            }))
    except Exception:
        pass
    return res


# Optional routers
try:
    from .routes.train import router as train_router
    app.include_router(train_router)
except Exception:
    pass

try:
    from .routes.oauth import router as oauth_router
    app.include_router(oauth_router)
except Exception:
    pass


try:
    from .routes.integrations import router as integrations_router
    app.include_router(integrations_router)
except Exception:
    pass

try:
    from .routes.auth import router as auth_router
    app.include_router(auth_router)
except Exception:
    pass


# WebSocket echo for audio
@app.websocket('/ws/audio')
async def websocket_audio(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f'ACK: {data[:200]}')
    except WebSocketDisconnect:
        pass


# WebSocket bridge for Electron clients
@app.websocket('/ws/bridge')
async def websocket_bridge(ws: WebSocket):
    await ws.accept()
    device_id = None
    try:
        query = dict(
            (x.split('=') for x in (ws.scope.get('query_string', '').decode().split('&') if ws.scope.get('query_string') else []))
        )
        token = query.get('token')
        if not token:
            await ws.close(code=1008)
            return
        if token.startswith('Bearer '):
            token = token.split(' ', 1)[1]
        from .auth import decode_token
        try:
            payload = decode_token(token)
        except Exception:
            await ws.close(code=1008)
            return
        device_id = payload.get('device_id')
        if not device_id:
            await ws.close(code=1008)
            return
        BRIDGE_CLIENTS[device_id] = ws
        while True:
            msg = await ws.receive_text()
            await ws.send_text('pong')
    except Exception:
        pass
    finally:
        if device_id and device_id in BRIDGE_CLIENTS:
            del BRIDGE_CLIENTS[device_id]


# ✅ Health check endpoint for Railway
@app.get("/health")
def health_check():
    return {"status": "ok"}



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run('backend.main:app', host='0.0.0.0', port=port, reload=False)
