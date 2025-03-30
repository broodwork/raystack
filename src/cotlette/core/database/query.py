from cotlette.core.database.backends.sqlite3 import db


class QuerySet:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = f"SELECT * FROM {model_class.__name__}"
        self.params = None

    def filter(self, **kwargs):
        conditions = " AND ".join([f"{key}=?" for key in kwargs])
        self.query += f" WHERE {conditions}"
        self.params = tuple(kwargs.values())
        return self

    def all(self):
        result = db.execute(self.query, self.params, fetch=True)
        return [self.model_class(**dict(zip(self.model_class._fields.keys(), row))) for row in result]

    def create(self, **kwargs):
        """
        Создает новую запись в базе данных.
        :param kwargs: Значения полей для новой записи.
        :return: Созданный экземпляр модели.
        """
        # Формируем список полей и значений для INSERT
        fields = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        values = tuple(kwargs.values())

        # Формируем SQL-запрос
        insert_query = f"INSERT INTO {self.model_class.__name__} ({fields}) VALUES ({placeholders})"

        # Выполняем запрос
        db.execute(insert_query, values)
        db.commit()  # Фиксируем изменения

        # Возвращаем созданный объект модели
        return self.model_class(**kwargs)
    
    def first(self):
        """
        Возвращает первый объект модели из результата запроса.
        Если записей нет, возвращает None.
        """
        # Добавляем LIMIT 1 к запросу
        query = f"{self.query} LIMIT 1"
        result = db.execute(query, self.params, fetch=True)

        if result:
            # Преобразуем первую строку в объект модели
            row = result[0]
            return self.model_class(**dict(zip(self.model_class._fields.keys(), row)))
        return None
    
    def save(self, instance):
        data = instance.__dict__

        if hasattr(instance, 'id') and instance.id is not None:
            # Обновление существующей записи
            fields = ', '.join([f"{key}=?" for key in data if key != 'id'])
            values = tuple(data[key] for key in data if key != 'id') + (instance.id,)
            update_query = f"UPDATE {self.model_class.__name__} SET {fields} WHERE id=?"
            db.execute(update_query, values)
            db.commit()
        else:
            # Создание новой записи
            fields = ', '.join([key for key in data if key != 'id'])
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data[key] for key in data if key != 'id')

            insert_query = f"INSERT INTO {self.model_class.__name__} ({fields}) VALUES ({placeholders})"
            db.execute(insert_query, values)
            db.commit()

            # Получаем id созданной записи
            instance.id = db.lastrowid

        return instance