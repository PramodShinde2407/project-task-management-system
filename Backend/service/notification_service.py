from sqlalchemy.orm import Session
from fastapi import HTTPException
from Backend.models.notifications import Notification
from Backend.schemas.notifications import NotificationUpdate


def get_all_notifications(db: Session):
    return db.query(Notification).all()


def get_notification(db: Session, notification_id: int):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return notification


def update_notification(
    db: Session,
    notification_id: int,
    notification_data: NotificationUpdate
):
    notification = get_notification(db, notification_id)

    update_data = notification_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(notification, key, value)

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(db: Session, notification_id: int):
    notification = get_notification(db, notification_id)

    db.delete(notification)
    db.commit()

    return {"message": "Notification deleted successfully"}