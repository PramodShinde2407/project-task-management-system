from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from Backend.models.tasks import Task
from Backend.models.projects import Project
from Backend.models.users import User
from Backend.models.projects_assigned import ProjectAssigned

from Backend.schemas.tasks import (
    TaskCreate,
    TaskUpdate
)

from Backend.core.enum import (
    UserRole,
    TaskStatus,
    TaskPriority
)


class TaskService:

    # =====================================================
    # Helper : Get Task
    # =====================================================

    def _get_task(
        self,
        db: Session,
        task_id: int
    ) -> Task:

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
    # Helper : Get Project
    # =====================================================

    def _get_project(
        self,
        db: Session,
        project_id: int
    ) -> Project:

        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found."
            )

        return project

    # =====================================================
    # Helper : Check Project Owner
    # =====================================================

    def _is_project_owner(
        self,
        project: Project,
        current_user: User
    ):

        return (
            current_user.role == UserRole.ADMIN
            or project.manager_id == current_user.id
        )

    # =====================================================
    # Create Task
    # =====================================================

    def create_task(
        self,
        db: Session,
        task_data: TaskCreate,
        current_user: User
    ):

        project = self._get_project(
            db,
            task_data.project_id
        )

        # Only Admin or Project Manager
        if not self._is_project_owner(
            project,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=TaskStatus.TODO,
            due_date=task_data.due_date,
            project_id=task_data.project_id,
            creator_id=current_user.id
        )

        try:

            db.add(task)

            db.commit()

            db.refresh(task)

            return task

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create task."
            )

    # =====================================================
    # Get Task
    # =====================================================

    def get_task(
        self,
        db: Session,
        task_id: int,
        current_user: User
    ):

        task = self._get_task(
            db,
            task_id
        )

        project = self._get_project(
            db,
            task.project_id
        )

        if self._is_project_owner(
            project,
            current_user
        ):
            return task

        assigned = (
            db.query(ProjectAssigned)
            .filter(
                ProjectAssigned.project_id == project.id,
                ProjectAssigned.user_id == current_user.id
            )
            .first()
        )

        if assigned:
            return task

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )


        # =====================================================
    # Get All Tasks
    # =====================================================

    def get_all_tasks(
        self,
        db: Session,
        current_user: User
    ):

        # Admin -> All Tasks
        if current_user.role == UserRole.ADMIN:
            return db.query(Task).all()

        # Manager -> Tasks of Managed Projects
        if current_user.role == UserRole.MANAGER:

            return (
                db.query(Task)
                .join(Project)
                .filter(Project.manager_id == current_user.id)
                .all()
            )

        # Team Member -> Tasks of Assigned Projects
        return (
            db.query(Task)
            .join(ProjectAssigned,
                  Task.project_id == ProjectAssigned.project_id)
            .filter(
                ProjectAssigned.user_id == current_user.id
            )
            .all()
        )


    # =====================================================
    # Update Task
    # =====================================================

    def update_task(
        self,
        db: Session,
        task_id: int,
        task_data: TaskUpdate,
        current_user: User
    ):

        task = self._get_task(
            db,
            task_id
        )

        project = self._get_project(
            db,
            task.project_id
        )

        if not self._is_project_owner(
            project,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        if task_data.title is not None:
            task.title = task_data.title

        if task_data.description is not None:
            task.description = task_data.description

        if task_data.due_date is not None:
            task.due_date = task_data.due_date

        if task_data.priority is not None:
            task.priority = task_data.priority

        if task_data.status is not None:
            task.status = task_data.status

        try:

            db.commit()

            db.refresh(task)

            return task

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update task."
            )


    # =====================================================
    # Delete Task
    # =====================================================

    def delete_task(
        self,
        db: Session,
        task_id: int,
        current_user: User
    ):

        task = self._get_task(
            db,
            task_id
        )

        project = self._get_project(
            db,
            task.project_id
        )

        if not self._is_project_owner(
            project,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        try:

            db.delete(task)

            db.commit()

            return {
                "message": "Task deleted successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete task."
            )
    
    from Backend.models.tasks_assigned import TaskAssigned


    # =====================================================
    # Assign Task
    # =====================================================

    def assign_task(
        self,
        db: Session,
        task_id: int,
        user_id: int,
        current_user: User
    ):

        task = self._get_task(db, task_id)

        project = self._get_project(db, task.project_id)

        if not self._is_project_owner(project, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        # Check User Exists
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

        # User must belong to project
        project_member = (
            db.query(ProjectAssigned)
            .filter(
                ProjectAssigned.project_id == project.id,
                ProjectAssigned.user_id == user.id
            )
            .first()
        )

        if project_member is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not assigned to this project."
            )

        # Prevent duplicate assignment
        existing = (
            db.query(TaskAssigned)
            .filter(
                TaskAssigned.task_id == task.id,
                TaskAssigned.task_assigned_user_id == user.id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already assigned."
            )

        assignment = TaskAssigned(
            task_id=task.id,
            task_assigned_user_id=user.id
        )

        try:

            db.add(assignment)

            db.commit()

            return {
                "message": "Task assigned successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Unable to assign task."
            )


    # =====================================================
    # Remove Assignee
    # =====================================================

    def remove_assignee(
        self,
        db: Session,
        task_id: int,
        user_id: int,
        current_user: User
    ):

        task = self._get_task(db, task_id)

        project = self._get_project(db, task.project_id)

        if not self._is_project_owner(project, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        assignment = (
            db.query(TaskAssigned)
            .filter(
                TaskAssigned.task_id == task.id,
                TaskAssigned.task_assigned_user_id == user_id
            )
            .first()
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found."
            )

        try:

            db.delete(assignment)

            db.commit()

            return {
                "message": "Assignee removed successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=500,
                detail="Unable to remove assignee."
            )


    # =====================================================
    # Get Task Assignees
    # =====================================================

    def get_task_assignees(
        self,
        db: Session,
        task_id: int,
        current_user: User
    ):

        task = self._get_task(db, task_id)

        project = self._get_project(db, task.project_id)

        if not self._is_project_owner(project, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        return (
            db.query(User)
            .join(
                TaskAssigned,
                User.id == TaskAssigned.task_assigned_user_id
            )
            .filter(
                TaskAssigned.task_id == task.id
            )
            .all()
        )


    # =====================================================
    # Update Task Status
    # =====================================================

    def update_status(
        self,
        db: Session,
        task_id: int,
        new_status: TaskStatus,
        current_user: User
    ):

        task = self._get_task(db, task_id)

        task.status = new_status

        db.commit()

        db.refresh(task)

        return task


    # =====================================================
    # Update Task Priority
    # =====================================================

    def update_priority(
        self,
        db: Session,
        task_id: int,
        new_priority: TaskPriority,
        current_user: User
    ):

        task = self._get_task(db, task_id)

        project = self._get_project(db, task.project_id)

        if not self._is_project_owner(project, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        task.priority = new_priority

        db.commit()

        db.refresh(task)

        return task



task_service = TaskService()