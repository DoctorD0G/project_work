import asyncio
import os
import sys
from pathlib import Path

BASE_DIR = os.path.abspath(Path(__file__).parents[2])
sys.path.append(BASE_DIR)

from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container, init_container
from domain.services.task import TaskServiceInterface


@inject
async def start_process(
    task_service: TaskServiceInterface = Provide[Container.task_service],
):
    pass


container = init_container()
container.wire(packages=[__name__])


if __name__ == "__main__":
    asyncio.run(start_process())
