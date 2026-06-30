from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Backend.database.session import get_db

from Backend.schemas.users import UserCreate, UserOut
from Backend.schemas.auth import UserLogin, LoginResponse
from Backend.core.security import get_current_user
from Backend.service.auth_service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# -------------------------------------------------------
# Register New User
# -------------------------------------------------------

@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return auth_service.signup(db, user)


# -------------------------------------------------------
# Login User
# -------------------------------------------------------

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    return auth_service.login(db, credentials)


# -------------------------------------------------------
# Logout User
# -------------------------------------------------------

@router.post("/logout")
def logout(
    current_user=Depends(get_current_user)
):
    return auth_service.logout()