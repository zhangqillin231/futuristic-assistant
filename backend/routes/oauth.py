
# backend/routes/oauth.py
from fastapi import APIRouter, HTTPException, Request
import os, urllib.parse

router = APIRouter(prefix='/oauth')

@router.get('/spotify/auth')
async def spotify_auth():
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    redirect = os.environ.get('SPOTIFY_REDIRECT_URI') or 'http://localhost:8000/oauth/spotify/callback'
    if not client_id:
        raise HTTPException(status_code=503, detail='SPOTIFY_CLIENT_ID not configured')
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect,
        'scope': 'user-modify-playback-state,user-read-playback-state',
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    return {'url': url}

@router.get('/spotify/callback')
async def spotify_callback(request: Request):
    # In production, exchange code for tokens and store securely
    code = request.query_params.get('code')
    return {'status':'ok', 'code': code}

@router.get('/gmail/auth')
async def gmail_auth():
    client_id = os.environ.get('GMAIL_CLIENT_ID')
    redirect = os.environ.get('GMAIL_REDIRECT_URI') or 'http://localhost:8000/oauth/gmail/callback'
    if not client_id:
        raise HTTPException(status_code=503, detail='GMAIL_CLIENT_ID not configured')
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect,
        'scope': 'https://www.googleapis.com/auth/gmail.send',
        'access_type': 'offline',
        'prompt':'consent'
    }
    url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
    return {'url': url}

@router.get('/gmail/callback')
async def gmail_callback(request: Request):
    code = request.query_params.get('code')
    return {'status':'ok', 'code': code}
