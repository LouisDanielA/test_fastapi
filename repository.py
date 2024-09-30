from sqlalchemy import select

from database import new_session, TaskOrm
from schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump() # model_dump() превращает объект модели в словарь

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush() # сохраняет в базу, без завершения транзакции
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all() # scalars фильтрация по модели запроса
            task_schemas = [STask.model_validate(task) for task in task_models]
            return task_schemas