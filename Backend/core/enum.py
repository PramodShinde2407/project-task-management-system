from enum import Enum

class UserRole(str,Enum):
    ADMIN="admin"
    MANAGER="manager"
    TEAM_MEMBER="team_member"
    

class TaskPriority(str,Enum):
    LOW="low"
    MEDIUM="medium"
    HIGH="high"
    CRITICAL="critical"

class TaskStatus(str,Enum):
    TODO="todo"
    IN_PROGRESS="in_progress"
    IN_REVIEW="in_review"
    BLOCKED="blocked"
    DONE="done"