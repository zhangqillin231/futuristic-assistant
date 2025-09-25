# 2050 Assistant - Futuristic Chatbot Ap

This project is a prototype "Siri++" ass
with:
- FastAPI backend (chat, actions, integr
- React + TypeScript frontend (futuristi
- Electron bridge for local device contr
- Training pipeline (RAG with FAISS and 
sentence-transformers)
- JWT auth, device registration, and aud

## Quick local run (backend)
1. cd backend
2. python -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. pip install sentence-transformers fai
pymongo
6. copy .env.example to .env and fill ke
7. uvicorn backend.main:app --reload --p
8000

## Electron bridge
1. cd electron
2. npm init -y
3. npm i electron ws
4. export BACKEND_WS=ws://localhost:8000
bridge
5. export DEVICE_TOKEN="Bearer 
<your_device_token>"
6. npx electron main.js

## Deploy
- Deploy backend on Render (use render.y
- Deploy frontend on Vercel (use vercel.
- Use MongoDB Atlas for DB and configure
MONGO_URI in .env

