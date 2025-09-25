
# 2050 Assistant - Futuristic Chatbot App

This project is a prototype "Siri++" assistant with:
- FastAPI backend (chat, actions, integrations)
- React + TypeScript frontend (futuristic UI)
- Electron bridge for local device control
- Training pipeline (RAG with FAISS and sentence-transformers)
- JWT auth, device registration, and audit logs

## Quick local run (backend)
1. cd backend
2. python -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. pip install sentence-transformers faiss-cpu pymongo
6. copy .env.example to .env and fill keys
7. uvicorn backend.main:app --reload --port 8000

## Electron bridge
1. cd electron
2. npm init -y
3. npm i electron ws
4. export BACKEND_WS=ws://localhost:8000/ws/bridge
5. export DEVICE_TOKEN="Bearer <your_device_token>"
6. npx electron main.js

## Deploy
- Deploy backend on Render (use render.yaml)
- Deploy frontend on Vercel (use vercel.json)
- Use MongoDB Atlas for DB and configure MONGO_URI in .env

