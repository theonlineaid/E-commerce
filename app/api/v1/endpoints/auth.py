from jose import JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import EmailPasswordLogin, AuthResponse, TokenPair
from app.services.auth_service import authenticate_user
from app.utils.security import create_tokens, verify_token
from app.db.session import get_db

router = APIRouter()
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login", response_model=AuthResponse, summary="User login with email/password")
async def login(
    credentials: EmailPasswordLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password
    
    - **email**: User's email address
    - **password**: User's password
    """
    try:
        user = authenticate_user(db, credentials.email, credentials.password)
        # return create_tokens({
        #     "sub": user.email,
        #     "role": user.role.value
        # })

        tokens = create_tokens({
            "sub": user.email,
            "role": user.role.value
        })
        
        # Return a SINGLE dictionary that matches AuthResponse
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": tokens["token_type"],
            "email": user.email,
            "role": user.role.value,
            "expires_at": datetime.utcnow() + timedelta(minutes=15)
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
   

@router.post("/refresh", response_model=TokenPair)
def refresh_token(
    refresh_token: str = Depends(reuseable_oauth)
):
    try:
        payload = verify_token(refresh_token)
        if not payload.get("refresh"):
            raise HTTPException(
                status_code=400,
                detail="Not a refresh token"
            )
        
        return create_tokens({
            "sub": payload["sub"],
            "role": payload["role"]
        })
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )