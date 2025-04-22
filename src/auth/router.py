from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.schemas import UserCreate, UserResponse, Token, LoginInput
from src.auth.service import (
    authenticate_user,
    create_access_token,
    register_user,
)
from src.db.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(form_data: LoginInput, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token}


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data)
