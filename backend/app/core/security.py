"""Security utilities for JWT and password handling."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with 12 rounds."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(user_id: str, email: str) -> str:
    """Create a JWT token for a user."""
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=settings.JWT_EXPIRATION_DAYS)

    payload = {
        "sub": user_id,
        "email": email,
        "iat": now,
        "exp": expires,
    }

    return jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """Extract user_id from a JWT token."""
    payload = decode_jwt_token(token)
    if payload:
        return payload.get("sub")
    return None
