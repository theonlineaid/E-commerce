# app/services/auth_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import verify_password, hash_password  # Import from your utils

def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email from database"""
    return db.query(User).filter(User.email == email).first()

def authenticate_user(
    db: Session, 
    email: str, 
    password: str
) -> User:
    """
    Authenticate a user with email and password
    Returns User object if valid, raises HTTPException otherwise
    
    Args:
        db: SQLAlchemy session
        email: User's email
        password: Plain text password
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: 401 for invalid credentials, 400 for inactive users
    """
    user = get_user_by_email(db, email)
    
    # Check user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            # headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password (using your existing utility)
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password does not match",
            # headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check account active status
    if not getattr(user, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account",
        )
    
    return user