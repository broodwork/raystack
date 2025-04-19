from pydantic import BaseModel
from typing import Optional
from cotlette.core.database.models import Model
from cotlette.core.database.fields import CharField, IntegerField, AutoField
from cotlette.core.database.fields.related import ForeignKeyField

from apps.groups.models import Group, GroupModel

# Pydantic-модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str
    group_id: int  # ID группы, к которой принадлежит пользователь
    organization: str = "N/A organization"

# Pydantic-модель для представления пользователя
class User(BaseModel):
    id: int
    name: str
    age: int
    email: str
    group: Optional[Group] = None
    organization: str = "N/A organization"

    # class Config:
    #     from_attributes = True

# Модель базы данных
class UserModel(Model):
    table = "users_usermodel"

    id = AutoField()  # Первичный ключ
    name = CharField(max_length=50)
    age = IntegerField()
    email = CharField(max_length=100)
    password_hash = CharField(max_length=255)
    group = ForeignKeyField(to="GroupModel", related_name="users")  # Связь с группой
    organization = CharField(max_length=100)
