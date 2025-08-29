from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Используем функционал фреймворка для работы с базой данных
from raystack.core.database.base import get_async_db

# Простая функция для получения текущего пользователя (заглушка)
async def get_current_user(session: AsyncSession = Depends(get_async_db)):
    # Здесь можно добавить логику аутентификации
    return None

