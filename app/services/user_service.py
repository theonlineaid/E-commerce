from app.models.user import User
from app.schemas.user import UserCreate
from app.db.session import SessionLocal
from app.utils.security import hash_password

def get_user_by_email(db: SessionLocal, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: SessionLocal, user: UserCreate):
    db_user = User(
        email=user.email,
        password=hash_password(user.password),
        full_name=user.full_name,
        username=user.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user