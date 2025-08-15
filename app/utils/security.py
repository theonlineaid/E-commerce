from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def create_tokens(
    data: dict,
    access_expires: timedelta = None,
    refresh_expires: timedelta = None
) -> dict:
    """Generate both access and refresh tokens"""
    access_expires = access_expires or timedelta(minutes=15)
    refresh_expires = refresh_expires or timedelta(days=7)
    
    access_data = data.copy()
    access_data.update({
        "exp": datetime.now(timezone.utc) + access_expires,
        "refresh": False
    })
    
    refresh_data = data.copy()
    refresh_data.update({
        "exp": datetime.now(timezone.utc) + refresh_expires,
        "refresh": True
    })
    
    return {
        "access_token": jwt.encode(
            access_data,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        ),
        "refresh_token": jwt.encode(
            refresh_data,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        ),
        "token_type": "bearer"
    }

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], tz=timezone.utc):
            raise JWTError("Token expired")
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
