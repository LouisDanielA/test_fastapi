from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter
from pydantic import BaseModel

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from repository import TaskRepository
from schemas import STaskAdd, STask, STaskId


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')

    await create_tables()
    print('База готова')

    yield
    print('Выключение')


app = FastAPI(lifespan=lifespan)

router = APIRouter(
    prefix='/tasks',
    tags=['Таски',]
)

tasks = []
@router.post('/')
async def add_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
    #tasks.append(task)
    task_id = await TaskRepository.add_one(task)
    return {'ok': True, 'task_id': task_id}
# pydantic всегда проверяет конвертацию возвращаемых данных
# к типу указанному в аннотации, в данном случае схема

@router.get('/list')
async def get_tasks() -> list[STask]:
    #task = Task(name="Сходи на рыбалку")
    tasks = await TaskRepository.find_all()
    return tasks


app.include_router(router)