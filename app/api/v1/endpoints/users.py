from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileResponse
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import get_user_by_email, create_user
from app.db.session import get_db
from app.utils.cloudinary_utils import ( upload_to_cloudinary, delete_from_cloudinary )
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/me", response_model=ProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@router.patch("/me/avatar", response_model=ProfileResponse)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Verify file is an image
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only image files are allowed"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Delete old avatar if exists
        if current_user.avatar_url:
            delete_from_cloudinary(current_user.avatar_url)
        
        # Upload new avatar
        current_user.avatar_url = upload_to_cloudinary(
            file_content,
            folder=f"users/{current_user.id}/avatars"
        )
        
        db.commit()
        db.refresh(current_user)
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Avatar update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update avatar"
        )
    finally:
        await file.close()

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Delete avatar if exists
        if current_user.avatar_url:
            delete_from_cloudinary(current_user.avatar_url)
        
        # Delete user from database
        db.delete(current_user)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Account deletion failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Account deletion failed"
        )