from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class ProfileBase(BaseModel):
    # username: str
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    phone_number: Optional[str] = Field(None, example="+1234567890")
    avatar_url: Optional[HttpUrl] = Field(None, example="https://res.cloudinary.com/...")

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    email: str
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True