from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.models.user import User
from app.utils.security import verify_token
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = verify_token(token)

    # Block refresh tokens
    if payload.get("refresh"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh tokens cannot be used for access"
        )

    # Assuming 'sub' in JWT contains the user's email
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db)
# ):
#     payload = verify_token(token)

#     if payload.get("refresh"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Refresh tokens cannot be used for access"
#         )

#     user_id = payload.get("sub")
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = await db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     return user


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = verify_token(token)
#     if payload.get("refresh"):
#         raise HTTPException(
#             status_code=403,
#             detail="Refresh tokens cannot be used for access"
#         )
#     return payload

def role_required(role: str):
    def checker(user: dict = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(
                status_code=403,
                detail=f"{role} privileges required"
            )
        return user
    return checker