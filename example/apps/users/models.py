from pydantic import BaseModel
from cotlette.core.database.models import Model
from cotlette.core.database.fields import CharField, IntegerField, AutoField
from cotlette.core.database.fields.related import ForeignKeyField


# Pydantic-модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str
    group_id: int  # ID группы, к которой принадлежит пользователь

# Pydantic-модель для представления пользователя
class User(BaseModel):
    id: int
    name: str
    age: int
    email: str
    group: dict  # Информация о группе, к которой принадлежит пользователь

# Модель базы данных
class UserModel(Model):
    id = AutoField()  # Первичный ключ
    name = CharField(max_length=50)
    age = IntegerField()
    email = CharField(max_length=100)
    password_hash = CharField(max_length=255)
    group = ForeignKeyField(to="GroupModel", related_name="users")  # Связь с группой

    def __str__(self):
        return self.name