
# Deploy Guide (short)

1. Create MongoDB Atlas free cluster. Get MONGO_URI.
2. On Render: create new web service from repo, link branch, set build & start commands as in render.yaml, and add env vars: MONGO_URI, JWT_SECRET, OPENAI_API_KEY, YOUTUBE_API_KEY, TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET.
3. On Vercel: connect repo and deploy. Set REACT_APP_API_URL to your Render backend URL.
4. For OAuth (Spotify/Gmail): configure redirect URIs to point to your Render backend (/oauth/spotify/callback and /oauth/gmail/callback).
5. Install Electron bridge locally and run with BACKEND_WS and DEVICE_TOKEN environment variables.
