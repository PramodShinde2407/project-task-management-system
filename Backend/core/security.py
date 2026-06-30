from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .config import settings
from Backend.database.session import get_db
from Backend.models.users import User


# OAuth2 will extract the Bearer token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------------------------------------------------
# Create JWT Access Token
# Called after successful login
# -------------------------------------------------------------------
def create_access_token(data: dict,expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME)
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# -------------------------------------------------------------------
# Decode and validate JWT
# Returns the payload if token is valid
# -------------------------------------------------------------------
def decode_access_token(token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception

        return payload

    except JWTError:
        raise credentials_exception


# -------------------------------------------------------------------
# Get currently logged-in user
# Used as dependency in protected routes
# -------------------------------------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    user_id = int(payload["sub"])

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user