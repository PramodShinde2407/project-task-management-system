from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from Backend.database.session import get_db
from Backend.schemas.notifications import (
    NotificationOut,
    NotificationUpdate,
)
from Backend.service.notification_service import (
    get_all_notifications,
    get_notification,
    update_notification,
    delete_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get("/", response_model=List[NotificationOut])
def read_all_notifications(db: Session = Depends(get_db)):
    return get_all_notifications(db)


@router.get("/{notification_id}", response_model=NotificationOut)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    return get_notification(db, notification_id)


@router.patch("/{notification_id}", response_model=NotificationOut)
def mark_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    db: Session = Depends(get_db),
):
    return update_notification(
        db,
        notification_id,
        notification_data,
    )


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    return delete_notification(db, notification_id)