from pydantic import BaseModel
from cotlette.core.database.models import Model
from cotlette.core.database.fields import CharField, AutoField

# Pydantic-модель для создания группы
class GroupCreate(BaseModel):
    name: str  # Название группы

# Pydantic-модель для представления группы
class Group(BaseModel):
    id: int
    name: str

    # class Config:
    #     from_attributes = True

# # Модель базы данных для групп
# class GroupModel(Model):
#     id = AutoField()  # Первичный ключ
#     name = CharField(max_length=100, unique=True)  # Название группы (уникальное)

#     def __str__(self):
#         return self.name

class GroupModel(Model):
    id = AutoField()  # Первичный ключ
    name = CharField(max_length=100, unique=True)  # Название группы (уникальное)

    @property
    def users(self):
        """
        Загружает всех пользователей, связанных с этой группой.
        """
        return UserModel.objects.filter(group=self.id)
