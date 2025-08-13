from datetime import datetime
from pydantic import BaseModel

class TokenBase(BaseModel):
    token_type: str
    expires_in: int  # Seconds until expiration

class EmailPasswordLogin(BaseModel):
    email: str
    password: str

class AccessToken(TokenBase):
    access_token: str

class RefreshToken(TokenBase):
    refresh_token: str

class TokenPair(BaseModel):
    """Response model containing both tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None
    refresh: bool = False  # Whether this is a refresh token claim

class UserLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type:  str = "bearer"
    email: str
    role: str
    expires_at: datetime