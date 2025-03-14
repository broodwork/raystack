from fastapi_orm.models import Model
from fastapi_orm.fields import CharField, IntegerField

class Book(Model):
    title = CharField(max_length=100)
    author = CharField(max_length=100)
    published_date = IntegerField()

# Создание таблицы
Book.create_table()

# new_book = Book.objects.create(
#     title="test1",
#     author="test2"
# )
books = Book.objects.all()
print('books', books)