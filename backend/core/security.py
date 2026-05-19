from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from core.config import settings
from core.exceptions import AuthenticationError

_hasher = PasswordHash([Argon2Hasher()])

ALGORITHM = "HS256"


def hash_password(plain: str) -> str:
    return _hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _hasher.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """Decode and validate a JWT, returning the subject (email). Raises AuthenticationError on failure."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        subject: str | None = payload.get("sub")
        if not subject:
            raise AuthenticationError("Token payload missing subject")
        return subject
    except ExpiredSignatureError as exc:
        raise AuthenticationError("Token has expired") from exc
    except InvalidTokenError as exc:
        raise AuthenticationError("Invalid token") from exc
