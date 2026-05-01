from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.dependencies import get_db_session
from core.exceptions import AuthenticationError
from core.security import create_access_token, verify_password
from models.schemas import Token, UserCreate, UserRead
from repositories.user_repo import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db_session)],
) -> UserRead:
    if UserRepository.get_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    user = UserRepository.create_user(db, user_in)
    return UserRead.model_validate(user)


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db_session)],
) -> Token:
    user = UserRepository.get_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise AuthenticationError("Incorrect email or password")
    if not user.is_active:
        raise AuthenticationError("Account is inactive")
    return Token(access_token=create_access_token(user.email))
