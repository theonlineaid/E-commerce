from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Schema for creating a user (input)"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str | None = Field(None, max_length=100)

class UserOut(BaseModel):
    """Schema for returning user data (output)"""
    id: int
    # email: EmailStr
    username: str
    # full_name: str | None
    # is_active: bool
    
    class Config:
        from_attributes = True  # Allows ORM model -> Pydantic conversion