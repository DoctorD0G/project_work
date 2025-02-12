import logging
from typing import Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, status

from domain.entities.task import (
    PaginableTaskFilter,
    CreateTask,
    UpdateTask,
    EntityId,
)
from domain.exceptions import InvalidTaskName
from domain.services.task import TaskServiceInterface
from infrastructure.container import Container
from infrastructure.permissions import TASK_VIEW_PERMISSION, TASK_EDIT_PERMISSION
from infrastructure.web.api.dependencies import (
    perm_check,
    app_status_paused,
    get_current_user,
)
from infrastructure.web.api.exceptions import FormFieldValidationException
from infrastructure.web.schemas.rest import TablePagination, PageDto

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", summary="Список задач")
@perm_check(TASK_VIEW_PERMISSION)
@inject
async def task_list(
    current_user=Depends(get_current_user),
    pagination_params=Depends(TablePagination),
    task_service: TaskServiceInterface = Depends(Provide[Container.task_service]),
) -> Any:
    """
    Список задач
    """
    try:
        paginable_filter = PaginableTaskFilter.parse_obj(pagination_params.filter)
        items, total = await task_service.get_paginable_tasks(
            pagination_params.page,
            pagination_params.size,
            pagination_params.sort_field,
            pagination_params.sort_descending,
            paginable_filter,
        )
        return PageDto(
            items=items,
            total=total,
            page=pagination_params.page,
            size=pagination_params.size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении списка задач",
        ) from e


@router.get("/{id}/", summary="Информация о задаче")
@perm_check(TASK_VIEW_PERMISSION)
@inject
async def task_detail(
    id: EntityId,
    task_service: TaskServiceInterface = Depends(Provide[Container.task_service]),
) -> Any:
    try:
        return await task_service.task_detail(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка: {e}"
        ) from e


@router.post("/", summary="Создать задачу")
@perm_check(TASK_EDIT_PERMISSION)
@app_status_paused
@inject
async def create_task(
    create_task: CreateTask,
    task_service: TaskServiceInterface = Depends(Provide[Container.task_service]),
) -> Any:
    try:
        return await task_service.create_task(create_task)
    except InvalidTaskName as e:
        # name - поле в котором произошла ошибка и само значение ошибки
        raise FormFieldValidationException(fields={"name": f"{e}"}) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания: {e}",
        ) from e


@router.put("/", summary="Изменить задачу")
@perm_check(TASK_EDIT_PERMISSION)
@app_status_paused
@inject
async def update_task(
    update_task: UpdateTask,
    task_service: TaskServiceInterface = Depends(Provide[Container.task_service]),
) -> Any:
    try:
        return await task_service.update_task(update_task)
    except InvalidTaskName as e:
        # name - поле в котором произошла ошибка и само значение ошибки
        raise FormFieldValidationException(fields={"name": f"{e}"}) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка изменения лимита: {e}",
        ) from e


@router.delete("/{id}/", summary="Удалить задачу")
@perm_check(TASK_EDIT_PERMISSION)
@app_status_paused
@inject
async def delete_task(
    id: EntityId,
    task_service: TaskServiceInterface = Depends(Provide[Container.task_service]),
) -> Any:
    try:
        return await task_service.delete_task(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка удаления: {e}",
        ) from e


@router.post("/upload/file/", summary="Загрузка файла")
@perm_check(TASK_EDIT_PERMISSION)
@app_status_paused
@inject
async def upload_file(
    name: str = Form(...),
    file: UploadFile | None = None,
) -> Any:
    print(name)
    print(file, type(file))
    return None
