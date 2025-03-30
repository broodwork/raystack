from cotlette.core.database.fields import CharField, IntegerField, Field
from cotlette.core.database.manager import Manager
from cotlette.core.database.backends.sqlite3 import db

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name != "Model":
            fields = {}
            for key, value in attrs.items():
                if isinstance(value, Field):
                    fields[key] = value
            attrs['_fields'] = fields
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    objects = Manager(None)

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.objects.model_class = cls

    @classmethod
    def create_table(cls):
        columns = []
        for field_name, field in cls._fields.items():
            column_def = f"{field_name} {field.column_type}"
            if field.primary_key:
                column_def += " PRIMARY KEY"
            columns.append(column_def)
        query = f"CREATE TABLE IF NOT EXISTS {cls.__name__} ({', '.join(columns)})"
        db.execute(query)  # Выполняем запрос на создание таблицы
        db.commit()        # Фиксируем изменения
    
    def save(self):
        """
        Сохраняет текущий объект в базе данных.
        Если объект уже существует (имеет id), выполняется UPDATE.
        Если объект новый (id отсутствует или равен None), выполняется INSERT.
        """
        # Получаем значения полей объекта
        data = {field: getattr(self, field, None) for field in self._fields}

        # Преобразуем значения в поддерживаемые SQLite типы
        def convert_value(value):
            if isinstance(value, (int, float, str, bytes, type(None))):
                return value
            elif hasattr(value, '__str__'):
                return str(value)  # Преобразуем объект в строку, если это возможно
            else:
                raise ValueError(f"Unsupported type for database: {type(value)}")

        data = {key: convert_value(value) for key, value in data.items()}

        # Проверяем, существует ли объект в базе данных
        if hasattr(self, 'id') and self.id is not None:
            # Обновляем существующую запись (UPDATE)
            fields = ', '.join([f"{key}=?" for key in data if key != 'id'])
            values = tuple(data[key] for key in data if key != 'id') + (self.id,)
            update_query = f"UPDATE {self.__class__.__name__} SET {fields} WHERE id=?"
            db.execute(update_query, values)
            db.commit()
        else:
            # Создаем новую запись (INSERT)
            fields = ', '.join([key for key in data if key != 'id'])
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data[key] for key in data if key != 'id')

            insert_query = f"INSERT INTO {self.__class__.__name__} ({fields}) VALUES ({placeholders})"
            db.execute(insert_query, values)
            db.commit()

            # Получаем id созданной записи
            self.id = db.lastrowid