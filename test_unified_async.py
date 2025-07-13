#!/usr/bin/env python3
"""
Тест объединенных async/sync методов
"""

import asyncio
import sys
import os

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cotlette.core.database.models import Model, CharField, IntegerField
from cotlette.core.database.backends.sqlite3 import SQLiteBackend
from cotlette.core.database.base import Database

# Настройка базы данных
db = Database()
db.set_backend(SQLiteBackend(':memory:'))

# Определяем тестовую модель
class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()
    
    class Meta:
        table_name = 'users'

# Создаем таблицу
db.create_table(User)

async def test_async_operations():
    """Тест асинхронных операций"""
    print("=== Тест асинхронных операций ===")
    
    # Создание
    user = await User.objects.create(name="Алексей", age=25)
    print(f"Создан пользователь: {user.name}, возраст: {user.age}")
    
    # Получение всех
    users = await User.objects.all().execute()
    print(f"Всего пользователей: {len(users)}")
    
    # Фильтрация
    young_users = await User.objects.filter(age__lt=30).execute()
    print(f"Молодых пользователей: {len(young_users)}")
    
    # Подсчет
    count = await User.objects.count()
    print(f"Общее количество: {count}")
    
    # Проверка существования
    exists = await User.objects.exists()
    print(f"Пользователи существуют: {exists}")

def test_sync_operations():
    """Тест синхронных операций"""
    print("=== Тест синхронных операций ===")
    
    # Создание
    user = User.objects.create(name="Мария", age=30)
    print(f"Создан пользователь: {user.name}, возраст: {user.age}")
    
    # Получение всех
    users = User.objects.all().execute()
    print(f"Всего пользователей: {len(users)}")
    
    # Фильтрация
    young_users = User.objects.filter(age__lt=30).execute()
    print(f"Молодых пользователей: {len(young_users)}")
    
    # Подсчет
    count = User.objects.count()
    print(f"Общее количество: {count}")
    
    # Проверка существования
    exists = User.objects.exists()
    print(f"Пользователи существуют: {exists}")

async def main():
    """Основная функция"""
    print("Начинаем тестирование объединенных async/sync методов...")
    
    # Тест синхронных операций
    test_sync_operations()
    
    # Тест асинхронных операций
    await test_async_operations()
    
    print("Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(main()) 