from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from Backend.models.users import User
from Backend.schemas.users import UserCreate, UserOut
from Backend.schemas.auth import UserLogin, LoginResponse

from Backend.utils.security import hash_password, verify_password
from Backend.core.security import create_access_token


class AuthService:

    # ----------------------------------------------------
    # Private Helper Methods
    # ----------------------------------------------------

    def _get_user_by_email(self, db: Session, email: str):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    def _get_user_by_username(self, db: Session, username: str):
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    # ----------------------------------------------------
    # Register New User
    # ----------------------------------------------------

    def signup(self, db: Session, user: UserCreate) -> UserOut:

        # Email already exists
        if self._get_user_by_email(db, user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered."
            )

        # Username already exists
        if self._get_user_by_username(db, user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken."
            )

        new_user = User(
            name=user.name,
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
            # role defaults to TEAM_MEMBER
        )

        try:

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create account."
            )
    # ----------------------------------------------------
    # Login User
    # ----------------------------------------------------

    def login(
        self,
        db: Session,
        credentials: UserLogin
    ) -> LoginResponse:

        # Find user by email
        user = self._get_user_by_email(
            db,
            credentials.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # Verify password
        if not verify_password(
            credentials.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        # Create JWT
        access_token = create_access_token(
            data={
                "sub": str(user.id)
            }
        )

        # Return Login Response
        return LoginResponse(
            access_token=access_token,
            token_type="Bearer",
            user=user
        )

    # ----------------------------------------------------
    # Logout User
    # ----------------------------------------------------

    def logout(self):

        # Stateless JWT
        # Frontend removes token from storage

        return {
            "message": "Logged out successfully."
        }


# ----------------------------------------------------
# Singleton Instance
# ----------------------------------------------------

auth_service = AuthService()