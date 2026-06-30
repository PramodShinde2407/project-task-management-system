from fastapi import FastAPI
from Backend.routes.auth_routes import router as auth_router
from Backend.routes.users_routes import router as user_router
from Backend.routes.projects_routes import router as project_router
from Backend.routes.tasks_routes import router as task_router
from Backend.routes.comments_routes import router as comment_router
from Backend.routes.notification_routes import router as notification_router

app=FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(comment_router)
app.include_router(notification_router)
