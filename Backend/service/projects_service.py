from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from Backend.models.projects import Project
from Backend.models.users import User

from Backend.schemas.projects import (
    ProjectCreate,
    ProjectUpdate
)

from Backend.core.enum import (
    UserRole,
    ProjectStatus
)
from Backend.models.projects_assigned import ProjectAssigned

class ProjectService:

    # =====================================================
    # Helper Methods
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
    # Create Project
    # =====================================================

    def create_project(
        self,
        db: Session,
        project_data: ProjectCreate,
        current_user: User
    ):

        # Only Admin or Manager
        if current_user.role not in [
            UserRole.ADMIN,
            UserRole.MANAGER
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        project = Project(
            name=project_data.name,
            description=project_data.description,
            start_date=project_data.start_date,
            end_date=project_data.end_date,
            status=ProjectStatus.PLANNED,
            manager_id=current_user.id
        )

        try:

            db.add(project)

            db.commit()

            db.refresh(project)

            return project

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create project."
            )

    # =====================================================
    # Get Project
    # =====================================================

    def get_project(
        self,
        db: Session,
        project_id: int,
        current_user: User
    ):

        project = self._get_project(
            db,
            project_id
        )

        # Admin can view everything
        if current_user.role == UserRole.ADMIN:
            return project

        # Manager can only view owned project
        if (
            current_user.role == UserRole.MANAGER
            and project.manager_id == current_user.id
        ):
            return project

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )

    # =====================================================
    # Get All Projects
    # =====================================================


    def get_all_projects(
        self,
        db: Session,
        current_user: User
    ):

        # Admin -> All projects
        if current_user.role == UserRole.ADMIN:
            return db.query(Project).all()

        # Manager -> Only owned projects
        if current_user.role == UserRole.MANAGER:
            return (
                db.query(Project)
                .filter(Project.manager_id == current_user.id)
                .all()
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied."
        )

    # =====================================================
    # Update Project
    # =====================================================

    def update_project(
        self,
        db: Session,
        project_id: int,
        project_data: ProjectUpdate,
        current_user: User
    ):

        project = self._get_project(
            db,
            project_id
        )

        # Only Admin or Project Owner
        if not self._is_project_owner(
            project,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        if project_data.name is not None:
            project.name = project_data.name

        if project_data.description is not None:
            project.description = project_data.description

        if project_data.start_date is not None:
            project.start_date = project_data.start_date

        if project_data.end_date is not None:
            project.end_date = project_data.end_date

        if project_data.status is not None:
            project.status = project_data.status

        try:

            db.commit()

            db.refresh(project)

            return project

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update project."
            )

    # =====================================================
    # Delete Project
    # =====================================================

    def delete_project(
        self,
        db: Session,
        project_id: int,
        current_user: User
    ):

        project = self._get_project(
            db,
            project_id
        )

        # Only Admin or Project Owner
        if not self._is_project_owner(
            project,
            current_user
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        try:

            db.delete(project)

            db.commit()

            return {
                "message": "Project deleted successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete project."
            )



    # =====================================================
    # Assign Member To Project
    # =====================================================

    def assign_member(
        self,
        db: Session,
        project_id: int,
        user_id: int,
        current_user: User
    ):

        project = self._get_project(db, project_id)

        # Only Admin or Project Owner
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

        # Prevent duplicate assignment
        existing_assignment = (
            db.query(ProjectAssigned)
            .filter(
                ProjectAssigned.project_id == project_id,
                ProjectAssigned.user_id == user_id
            )
            .first()
        )

        if existing_assignment:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already assigned."
            )

        assignment = ProjectAssigned(
            project_id=project_id,
            user_id=user_id
        )

        try:

            db.add(assignment)
            db.commit()

            return {
                "message": "Member assigned successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to assign member."
            )


    # =====================================================
    # Remove Member
    # =====================================================

    def remove_member(
        self,
        db: Session,
        project_id: int,
        user_id: int,
        current_user: User
    ):

        project = self._get_project(db, project_id)

        if not self._is_project_owner(project, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        assignment = (
            db.query(ProjectAssigned)
            .filter(
                ProjectAssigned.project_id == project_id,
                ProjectAssigned.user_id == user_id
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
                "message": "Member removed successfully."
            }

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to remove member."
            )


    # =====================================================
    # Get Project Members
    # =====================================================

    def get_project_members(
        self,
        db: Session,
        project_id: int,
        current_user: User
    ):

        project = self._get_project(db, project_id)

        if not self._is_project_owner(project, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied."
            )

        members = (
            db.query(User)
            .join(
                ProjectAssigned,
                User.id == ProjectAssigned.user_id
            )
            .filter(
                ProjectAssigned.project_id == project_id
            )
            .all()
        )

        return members


project_service = ProjectService()