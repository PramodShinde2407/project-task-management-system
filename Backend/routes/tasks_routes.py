from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Backend.database.session import get_db
from Backend.core.security import get_current_user

from Backend.models.users import User

from Backend.schemas.tasks import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskStatusUpdate,
    TaskPriorityUpdate,
    TaskAssign
)

from Backend.service.tasks_service import task_service


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =====================================================
# Create Task
# =====================================================
@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.create_task(
        db,
        task,
        current_user
    )


# =====================================================
# Get All Tasks
# =====================================================
@router.get(
    "/",
    response_model=list[TaskOut]
)
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.get_all_tasks(
        db,
        current_user
    )


# =====================================================
# Get Task By Id
# =====================================================
@router.get(
    "/{task_id}",
    response_model=TaskOut
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.get_task(
        db,
        task_id,
        current_user
    )


# =====================================================
# Update Task
# =====================================================
@router.patch(
    "/{task_id}",
    response_model=TaskOut
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.update_task(
        db,
        task_id,
        task,
        current_user
    )


# =====================================================
# Delete Task
# =====================================================
@router.delete(
    "/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.delete_task(
        db,
        task_id,
        current_user
    )


# =====================================================
# Assign User To Task
# =====================================================
@router.post(
    "/{task_id}/assign"
)
def assign_task(
    task_id: int,
    assignment: TaskAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.assign_task(
        db,
        task_id,
        assignment.user_id,
        current_user
    )


# =====================================================
# Remove Assignee
# =====================================================
@router.delete(
    "/{task_id}/assign/{user_id}"
)
def remove_assignee(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.remove_assignee(
        db,
        task_id,
        user_id,
        current_user
    )


# =====================================================
# Get Task Assignees
# =====================================================
@router.get(
    "/{task_id}/assignees"
)
def get_task_assignees(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.get_task_assignees(
        db,
        task_id,
        current_user
    )


# =====================================================
# Update Task Status
# =====================================================
@router.patch(
    "/{task_id}/status",
    response_model=TaskOut
)
def update_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.update_status(
        db,
        task_id,
        status_data.status,
        current_user
    )


# =====================================================
# Update Task Priority
# =====================================================
@router.patch(
    "/{task_id}/priority",
    response_model=TaskOut
)
def update_priority(
    task_id: int,
    priority_data: TaskPriorityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return task_service.update_priority(
        db,
        task_id,
        priority_data.priority,
        current_user
    )