from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Backend.database.session import get_db
from Backend.core.security import get_current_user

from Backend.models.users import User

from Backend.schemas.comments import (
    CommentCreate,
    CommentUpdate,
    CommentOut
)

from Backend.service.comments_service import comment_service


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


# =====================================================
# Create Comment
# POST /comments/tasks/{task_id}
# =====================================================
@router.post(
    "/tasks/{task_id}",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    task_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return comment_service.create_comment(
        db,
        task_id,
        comment,
        current_user
    )


# =====================================================
# Get All Comments of Task
# GET /comments/tasks/{task_id}
# =====================================================
@router.get(
    "/tasks/{task_id}",
    response_model=list[CommentOut]
)
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return comment_service.get_comments(
        db,
        task_id
    )


# =====================================================
# Update Comment
# PATCH /comments/{comment_id}
# =====================================================
@router.patch(
    "/{comment_id}",
    response_model=CommentOut
)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return comment_service.update_comment(
        db,
        comment_id,
        comment,
        current_user
    )


# =====================================================
# Delete Comment
# DELETE /comments/{comment_id}
# =====================================================
@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_200_OK
)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return comment_service.delete_comment(
        db,
        comment_id,
        current_user
    )