
# backend/routes/integrations.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import os, requests
from ..auth import verify_token as verify_token_header, SECRET

router = APIRouter(prefix='/integrations')

class YouTubeSearchRequest(BaseModel):
    q: str
    maxResults: int = 3

@router.post('/youtube/search')
async def youtube_search(req: YouTubeSearchRequest, token_payload: dict = Depends(verify_token_header)):
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        raise HTTPException(status_code=503, detail='YOUTUBE_API_KEY not configured')
    params = {'part':'snippet', 'q': req.q, 'type':'video', 'maxResults': req.maxResults, 'key': api_key}
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=params, timeout=10)
    r.raise_for_status()
    items = r.json().get('items', [])
    results = []
    for it in items:
        vid = it['id']['videoId']
        title = it['snippet']['title']
        url = f'https://www.youtube.com/watch?v={vid}'
        results.append({'title': title, 'videoId': vid, 'url': url})
    return {'results': results}

class TwilioSMSRequest(BaseModel):
    to: str
    body: str

@router.post('/twilio/sms')
async def twilio_sms(req: TwilioSMSRequest, token_payload: dict = Depends(verify_token_header)):
    sid = os.environ.get('TWILIO_SID')
    auth = os.environ.get('TWILIO_AUTH_TOKEN')
    from_num = os.environ.get('TWILIO_FROM_NUMBER')
    if not (sid and auth and from_num):
        raise HTTPException(status_code=503, detail='Twilio credentials not configured')
    url = f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json'
    data = {'From': from_num, 'To': req.to, 'Body': req.body}
    r = requests.post(url, data=data, auth=(sid, auth), timeout=10)
    r.raise_for_status()
    return {'ok': True, 'twilio': r.json()}

# Spotify and Gmail placeholders (require OAuth flows)
@router.post('/spotify/play')
async def spotify_play():
    raise HTTPException(status_code=501, detail='Spotify integration must be configured with OAuth tokens')

@router.post('/gmail/send')
async def gmail_send():
    raise HTTPException(status_code=501, detail='Gmail integration must be configured with OAuth credentials')
