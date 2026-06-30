from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from Backend.models.users import User
from Backend.schemas.users import UserUpdate
from Backend.core.enum import UserRole


class UserService:

    # ----------------------------------------------------
    # Private Helper
    # ----------------------------------------------------

    def _get_user_by_id(
        self,
        db: Session,
        user_id: int
    ) -> User:

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        return user

    # ----------------------------------------------------
    # Get All Users
    # ----------------------------------------------------

    def get_all_users(
        self,
        db: Session
    ):

        return db.query(User).all()

    # ----------------------------------------------------
    # Get User By Id
    # ----------------------------------------------------

    def get_user(
        self,
        db: Session,
        user_id: int
    ):

        return self._get_user_by_id(
            db,
            user_id
        )

    # ----------------------------------------------------
    # Update User
    # ----------------------------------------------------

    def update_user(
        self,
        db: Session,
        user_id: int,
        user_data: UserUpdate
    ):

        user = self._get_user_by_id(
            db,
            user_id
        )

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:

            existing_user = (
                db.query(User)
                .filter(
                    User.email == user_data.email,
                    User.id != user.id
                )
                .first()
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists."
                )

            user.email = user_data.email

        try:

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update user."
            )

    # ----------------------------------------------------
    # Delete User
    # ----------------------------------------------------

    def delete_user(
        self,
        db: Session,
        user_id: int
    ):

        user = self._get_user_by_id(
            db,
            user_id
        )

        try:

            db.delete(user)
            db.commit()

            return {
                "message": "User deleted successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete user."
            )

    # ----------------------------------------------------
    # Change User Role
    # ----------------------------------------------------

    def update_role(
        self,
        db: Session,
        user_id: int,
        role: UserRole
    ):

        user = self._get_user_by_id(
            db,
            user_id
        )

        user.role = role

        try:

            db.commit()
            db.refresh(user)

            return user

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update role."
            )


user_service = UserService()