from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Header
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas import TokenData, UserCreate
from src.common.exceptions import DuplicateEntryException, UnauthorizedException, UnauthenticatedException
from src.common.logger import get_logger
from src.config import settings
from src.db.database import get_db

logger = get_logger(__name__)

# Should go in env
SECRET_KEY = settings.SECRET_KEY
HASH_ALGORITHM = settings.HASH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedException("Invalid credentials")
    return user


def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: Session = Depends(get_db),
) -> User:
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise UnauthenticatedException("Invalid auth scheme")
    except ValueError:
        raise UnauthenticatedException("Invalid Authorization header format")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        username = payload.get("sub")
        if not username:
            logger.warning("Token missing subject")
            raise UnauthenticatedException("Invalid token payload")
        token_data = TokenData(username=username)
    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        raise UnauthenticatedException("Invalid token")

    user = get_user_by_username(db, token_data.username)
    if user is None:
        logger.warning("Token user not found in database")
        raise UnauthenticatedException("User not found")

    logger.debug(f"Authenticated user: {user.username}")
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise UnauthorizedException("Admin access required")
    return current_user


def register_user(db: Session, user_data: UserCreate) -> User:
    if db.query(User).filter(User.username == user_data.username).first():
        raise DuplicateEntryException("Username already registered")
    hashed_password = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
