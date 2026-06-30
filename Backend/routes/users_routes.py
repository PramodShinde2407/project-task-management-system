from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from Backend.database.session import get_db
from Backend.core.security import get_current_user
from Backend.core.enum import UserRole

from Backend.models.users import User
from Backend.schemas.users import (
    UserOut,
    UserUpdate,
)
from Backend.service.user_service import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ---------------------------------------------------------
# Get All Users (Admin Only)
# ---------------------------------------------------------
@router.get(
    "/",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return user_service.get_all_users(db)


# ---------------------------------------------------------
# Get User By Id
# Admin -> Any User
# User -> Own Profile
# ---------------------------------------------------------
@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return user_service.get_user(
        db,
        user_id
    )


# ---------------------------------------------------------
# Update User
# Admin -> Any User
# User -> Own Profile
# ---------------------------------------------------------
@router.patch(
    "/{user_id}",
    response_model=UserOut
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return user_service.update_user(
        db,
        user_id,
        user_data
    )


# ---------------------------------------------------------
# Delete User (Admin Only)
# ---------------------------------------------------------
@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return user_service.delete_user(
        db,
        user_id
    )