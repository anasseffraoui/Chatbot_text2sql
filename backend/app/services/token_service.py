from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from ..config import settings

_serializer = URLSafeTimedSerializer(settings.HMAC_SECRET)

def sign(payload: dict) -> str:
    return _serializer.dumps(payload)

def verify(token: str, max_age: int):
    try:
        return _serializer.loads(token, max_age=max_age)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
