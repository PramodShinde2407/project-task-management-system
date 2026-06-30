from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from Backend.database.session import get_db
from Backend.core.security import get_current_user
from Backend.core.enum import UserRole

from Backend.models.users import User

from Backend.schemas.projects import (
    ProjectCreate,
    ProjectUpdate,
    ProjectOut,
)

from Backend.service.projects_service import project_service


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# =====================================================
# Create Project
# Admin / Manager
# =====================================================
@router.post(
    "/",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.create_project(
        db,
        project,
        current_user
    )


# =====================================================
# Get All Projects
# =====================================================
@router.get(
    "/",
    response_model=list[ProjectOut]
)
def get_all_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.get_all_projects(
        db,
        current_user
    )


# =====================================================
# Get Project
# =====================================================
@router.get(
    "/{project_id}",
    response_model=ProjectOut
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.get_project(
        db,
        project_id,
        current_user
    )


# =====================================================
# Update Project
# =====================================================
@router.patch(
    "/{project_id}",
    response_model=ProjectOut
)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.update_project(
        db,
        project_id,
        project,
        current_user
    )


# =====================================================
# Delete Project
# =====================================================
@router.delete(
    "/{project_id}"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.delete_project(
        db,
        project_id,
        current_user
    )


# =====================================================
# Assign Member
# POST /projects/{project_id}/members
# =====================================================
@router.post(
    "/{project_id}/members"
)
def assign_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.assign_member(
        db,
        project_id,
        user_id,
        current_user
    )


# =====================================================
# Remove Member
# DELETE /projects/{project_id}/members/{user_id}
# =====================================================
@router.delete(
    "/{project_id}/members/{user_id}"
)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.remove_member(
        db,
        project_id,
        user_id,
        current_user
    )


# =====================================================
# Get Project Members
# =====================================================
@router.get(
    "/{project_id}/members"
)
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return project_service.get_project_members(
        db,
        project_id,
        current_user
    )