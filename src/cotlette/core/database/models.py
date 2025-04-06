from cotlette.core.database.fields import CharField, IntegerField, Field
from cotlette.core.database.manager import Manager
from cotlette.core.database.backends.sqlite3 import db
from cotlette.core.database.fields import ForeignKeyField


class ModelMeta(type):
    _registry = {}  # Словарь для хранения зарегистрированных моделей

    def __new__(cls, name, bases, attrs):
        # Создаем новый класс
        new_class = super().__new__(cls, name, bases, attrs)

        # Регистрируем модель в реестре, если это не базовый класс Model
        if name != "Model":
            cls._registry[name] = new_class

        # Собираем поля в словарь _fields
        fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):  # Проверяем, является ли атрибут экземпляром Field
                fields[attr_name] = attr_value

        # Присоединяем _fields к классу
        new_class._fields = fields
        return new_class

    @classmethod
    def get_model(cls, name):
        """
        Возвращает модель по имени из реестра.
        """
        return cls._registry.get(name)


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
        foreign_keys = []

        for field_name, field in cls._fields.items():
            # Формируем определение столбца
            column_def = f'"{field_name}" {field.column_type}'
            if field.primary_key:
                column_def += " PRIMARY KEY"
            if field.unique:
                column_def += " UNIQUE"
            columns.append(column_def)

            # Проверяем, является ли поле внешним ключом
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                foreign_keys.append(
                    f'FOREIGN KEY ("{field_name}") REFERENCES "{related_model.__name__}"("id")'
                )

        # Объединяем колонки и внешние ключи в один список
        all_parts = columns + foreign_keys

        # Формируем финальный SQL-запрос
        query = f'CREATE TABLE IF NOT EXISTS "{cls.__name__}" ({", ".join(all_parts)});'

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
