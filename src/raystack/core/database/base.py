from typing import AsyncGenerator, Generator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from raystack.conf import settings

# Синхронный движок
sync_engine = create_engine(settings.DATABASES["default"]["URL"], echo=True, future=True)

# Асинхронный движок (создаем только если URL поддерживает асинхронность)
async_engine = None
async_session_factory = None

try:
    if "aiosqlite" in settings.DATABASES["default"]["URL"] or "asyncpg" in settings.DATABASES["default"]["URL"] or "aiomysql" in settings.DATABASES["default"]["URL"]:
        async_engine = create_async_engine(settings.DATABASES["default"]["URL"], echo=True, future=True)
        async_session_factory = sessionmaker(bind=async_engine, class_=AsyncSession)
except Exception:
    # Если не удалось создать асинхронный движок, оставляем None
    pass

# Создание фабрик сессий
sync_session_factory = sessionmaker(bind=sync_engine, class_=Session)

async def create_db_and_tables():
    if async_engine:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    else:
        # Если асинхронный движок недоступен, используем синхронный
        SQLModel.metadata.create_all(sync_engine)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

def get_sync_db() -> Generator[Session, None, None]:
    with sync_session_factory() as session:
        yield session