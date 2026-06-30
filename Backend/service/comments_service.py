import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from Backend.models.comments import Comment
from Backend.models.tasks import Task
from Backend.models.users import User
from Backend.models.comments_mention import CommentMention

from Backend.schemas.comments import (
    CommentCreate,
    CommentUpdate
)


class CommentService:

    # =====================================================
    # Helper : Get Task
    # =====================================================

    def _get_task(
        self,
        db: Session,
        task_id: int
    ):

        task = (
            db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )

        return task

    # =====================================================
    # Helper : Get Comment
    # =====================================================

    def _get_comment(
        self,
        db: Session,
        comment_id: int
    ):

        comment = (
            db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found."
            )

        return comment

    # =====================================================
    # Helper : Save Mentions
    # =====================================================

    def _save_mentions(
        self,
        db: Session,
        comment: Comment
    ):

        # Example:
        # "Hello @john @alice"

        usernames = re.findall(
            r'@(\w+)',
            comment.comment
        )

        if not usernames:
            return

        users = (
            db.query(User)
            .filter(User.username.in_(usernames))
            .all()
        )

        for user in users:

            mention = CommentMention(
                comment_id=comment.id,
                user_id=user.id
            )

            db.add(mention)

    # =====================================================
    # Create Comment
    # =====================================================

    def create_comment(
        self,
        db: Session,
        task_id: int,
        comment_data: CommentCreate,
        current_user: User
    ):

        self._get_task(
            db,
            task_id
        )

        comment = Comment(
            comment=comment_data.comment,
            task_id=task_id,
            user_id=current_user.id
        )

        try:

            db.add(comment)

            db.flush()

            self._save_mentions(
                db,
                comment
            )

            db.commit()

            db.refresh(comment)

            return comment

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create comment."
            )

    # =====================================================
    # Get Comments of Task
    # =====================================================

    def get_comments(
        self,
        db: Session,
        task_id: int
    ):

        self._get_task(
            db,
            task_id
        )

        return (
            db.query(Comment)
            .filter(Comment.task_id == task_id)
            .order_by(Comment.created_at.asc())
            .all()
        )


        # =====================================================
    # Helper : Can Modify Comment
    # =====================================================

    def _can_modify_comment(
        self,
        comment: Comment,
        current_user: User
    ):

        return (
            current_user.role.name == "ADMIN"
            or comment.user_id == current_user.id
        )

    # =====================================================
    # Update Comment
    # =====================================================

    def update_comment(
        self,
        db: Session,
        comment_id: int,
        comment_data: CommentUpdate,
        current_user: User
    ):

        comment = self._get_comment(
            db,
            comment_id
        )

        if not self._can_modify_comment(
            comment,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        if comment_data.comment is not None:
            comment.comment = comment_data.comment

        try:

            # Remove old mentions
            db.query(CommentMention).filter(
                CommentMention.comment_id == comment.id
            ).delete()

            db.flush()

            # Save new mentions
            self._save_mentions(
                db,
                comment
            )

            db.commit()

            db.refresh(comment)

            return comment

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update comment."
            )


    # =====================================================
    # Delete Comment
    # =====================================================

    def delete_comment(
        self,
        db: Session,
        comment_id: int,
        current_user: User
    ):

        comment = self._get_comment(
            db,
            comment_id
        )

        if not self._can_modify_comment(
            comment,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        try:

            # Delete mentions first
            db.query(CommentMention).filter(
                CommentMention.comment_id == comment.id
            ).delete()

            db.delete(comment)

            db.commit()

            return {
                "message": "Comment deleted successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete comment."
            )




comment_service = CommentService()