from fastapi import APIRouter

from infrastructure.web.api.api_v1.endpoints import task, app_manager

api_router = APIRouter()

api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(
    app_manager.router, prefix="/app-manager", tags=["app_manager"]
)
