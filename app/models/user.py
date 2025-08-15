from enum import Enum
from sqlalchemy import Column, String, Boolean, Integer,  Enum as SQLEnum
from app.db.session import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)