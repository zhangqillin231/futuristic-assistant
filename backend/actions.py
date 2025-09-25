
# backend/actions.py (updated with audit logging and ownership checks)
from pydantic import BaseModel
from typing import Any, Dict
import logging
import os
from pymongo import MongoClient

logger = logging.getLogger(__name__)
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URI)
db = client.get_default_database() or client['assistant_db']

class ActionRequest(BaseModel):
    name: str
    params: Dict[str, Any] = {}
    user_confirmed: bool = False
    device_id: str | None = None
    user_id: str | None = None

# Whitelist: map safe action names to handlers
def _open_url(params):
    url = params.get('url')
    if not url:
        return {'error': 'missing_url'}
    return {'ok': True, 'action': 'open_url', 'url': url}

def _set_volume(params):
    level = params.get('level')
    if level is None:
        return {'error': 'missing_level'}
    try:
        level = int(level)
    except:
        return {'error': 'invalid_level'}
    if not (0 <= level <= 100):
        return {'error': 'level_out_of_range'}
    return {'ok': True, 'action': 'set_volume', 'level': level}

def _play_sound(params):
    sound = params.get('sound', 'default')
    return {'ok': True, 'action': 'play_sound', 'sound': sound}

ACTION_WHITELIST = {
    'open_url': _open_url,
    'set_volume': _set_volume,
    'play_sound': _play_sound,
}


def _log_audit(entry: Dict[str, Any]):
    try:
        db.audits.insert_one(entry)
    except Exception:
        logger.exception('Failed to write audit log')


def execute_action(req: ActionRequest, token_payload: Dict[str, Any] | None = None):
    # Security checks
    if req.name not in ACTION_WHITELIST:
        logger.warning('Attempt to call non-whitelisted action: %s', req.name)
        return {'error': 'action_not_allowed'}
    if not req.user_confirmed:
        return {'error': 'user_confirmation_required'}

    # Verify ownership: token_payload should contain device_id and owner
    if token_payload:
        token_device = token_payload.get('device_id')
        token_owner = token_payload.get('owner')
        if req.device_id and token_device != req.device_id:
            return {'error': 'device_mismatch'}
    # Log the requested action (audit), do not perform destructive ops here
    audit_entry = {
        'action': req.name,
        'params': req.params,
        'device_id': req.device_id,
        'user_id': req.user_id,
        'token_owner': token_payload.get('owner') if token_payload else None,
        'timestamp': __import__('time').time(),
    }
    _log_audit(audit_entry)

    handler = ACTION_WHITELIST[req.name]
    try:
        result = handler(req.params)
        # Log success
        _log_audit({**audit_entry, 'result': result, 'status': 'success'})
        return {'ok': True, 'result': result}
    except Exception as e:
        logger.exception('Action handler error')
        _log_audit({**audit_entry, 'status': 'error', 'error': str(e)})
        return {'error': 'handler_exception', 'message': str(e)}
