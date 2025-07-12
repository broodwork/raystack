import bcrypt
from typing import Union
from datetime import datetime, timedelta
import jwt

from config.settings import SECRET_KEY, ALGORITHM


# # Хешируем пароль с использованием bcrypt
# def hash_password(password: str) -> str:
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# # Проверяем, совпадает ли пароль
# def check_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

import asyncio

def asyncify(func):
    async def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        func_out = await loop.run_in_executor(None, func, *args, **kwargs)
        return func_out
    return inner

@asyncify
def hash_password(password: str):
    # Возвращаем строку для сохранения в базу данных
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@asyncify
def check_password(password: str, hashed_pass):
    # Если hashed_pass - это строка (из базы данных), кодируем её в байты
    if isinstance(hashed_pass, str):
        hashed_pass = hashed_pass.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pass)

# @asyncify
# def check_password(password: str, hashed_pass: str):
#     return bcrypt.checkpw(
#         password.encode('utf-8'),  # Преобразуем пароль в байты
#         hashed_pass.encode('utf-8')  # Преобразуем хэшированный пароль в байты
#     )

# Функция для создания JWT-токена
def generate_jwt(user_id: int):
    payload = {'user_id': user_id}
    # token = jwt.encode(payload, str(SECRET_KEY), algorithm=ALGORITHM).decode('utf-8')
    token = jwt.encode(payload, str(SECRET_KEY), algorithm=ALGORITHM)
    return token