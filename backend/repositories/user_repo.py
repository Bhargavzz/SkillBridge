from sqlalchemy import select
from sqlalchemy.orm import Session

from models.orm import User
from models.schemas import UserCreate
from core.security import hash_password


class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return db.execute(statement).scalar_one_or_none()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
