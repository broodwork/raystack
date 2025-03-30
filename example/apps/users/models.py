# from cotlette.db import models

from pydantic import BaseModel
from cotlette.core.database.models import Model
from cotlette.core.database.fields import CharField, IntegerField, AutoField
import bcrypt

# Pydantic-модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str

# Pydantic-модель для представления пользователя
class User(BaseModel):
    name: str
    age: int
    email: str

# Модель базы данных
class UserModel(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    age = IntegerField()
    # email = CharField(max_length=100, unique=True)
    email = CharField(max_length=100)
    password_hash = CharField(max_length=255)

    @classmethod
    def create_user(cls, user: UserCreate):
        # Хешируем пароль
        hashed_password = cls.hash_password(user.password)
        return cls.objects.create(
            name=user.name,
            age=user.age,
            email=user.email,
            password_hash=hashed_password
        )
