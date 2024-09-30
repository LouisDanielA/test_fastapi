from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    'sqlite+aiosqlite:///tasks.db'
)

new_session = async_sessionmaker(engine, expire_on_commit=False)
# expire_on_commit после коммита не будет вызывать новых запросов к базе данных
# new_session это фабрика сессии

class Base(DeclarativeBase):
    pass

class TaskOrm(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# run_sync запуск синхронных фукнции в асинхронном контексте

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

