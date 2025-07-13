from cotlette.core.database.sqlalchemy import db
from cotlette.core.database.fields.related import ForeignKeyField


class QuerySet:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = f'SELECT * FROM "{model_class.get_table_name()}"'
        self.params = None
        self.order_by_fields = []

    def filter(self, **kwargs):
        # Create new QuerySet for query chaining
        new_queryset = QuerySet(self.model_class)
        conditions = []

        for field_name, value in kwargs.items():
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")

            field = self.model_class._fields[field_name]

            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id  # Extract id if model object is passed
                elif not isinstance(value, int):
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")

            # Вставляем значение напрямую в запрос для SQLAlchemy
            if isinstance(value, str):
                conditions.append(f'"{field_name}"=\'{value}\'')
            else:
                conditions.append(f'"{field_name}"={value}')

        # Form new query with conditions
        new_queryset.query = f"{self.query} WHERE {' AND '.join(conditions)}"
        new_queryset.params = None  # Не используем параметры для SQLAlchemy
        return new_queryset
    
    def all(self):
        """
        Returns QuerySet with all objects.
        :return: New QuerySet.
        """
        return self

    def first(self):
        # Add LIMIT 1 to current query
        query = f"{self.query} LIMIT 1"
        result = db.execute(query, self.params or (), fetch=True)

        if result:
            row = result[0]
            return self.model_class(**{
                key: value for key, value in zip(self.model_class._fields.keys(), row)
                if key in self.model_class._fields
            })
        return None
    
    def order_by(self, *fields):
        """
        Adds sorting to query.
        :param fields: Fields for sorting (e.g., 'id', '-age').
        :return: New QuerySet with added sorting.
        """
        new_queryset = QuerySet(self.model_class)
        new_queryset.query = self.query
        new_queryset.params = self.params
        new_queryset.order_by_fields = list(fields)  # Save sorting fields

        # Add ORDER BY to query
        order_conditions = []
        for field in fields:
            if field.startswith('-'):
                # Descending sort
                order_conditions.append(f'"{field[1:]}" DESC')
            else:
                # Ascending sort
                order_conditions.append(f'"{field}" ASC')

        if order_conditions:
            new_queryset.query += f" ORDER BY {', '.join(order_conditions)}"

        return new_queryset

    def execute(self):
        # Execute current query and return result
        result = db.execute(self.query, self.params or (), fetch=True)
        return [
            self.model_class(**dict(zip(self.model_class._fields.keys(), row)))
            for row in result
        ]

    def create(self, **kwargs):
        fields = []
        values = []

        for field_name, value in kwargs.items():
            # Проверяем, существует ли поле в текущей модели
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")

            field = self.model_class._fields[field_name]

            # Обработка внешних ключей
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id  # Извлекаем id, если передан объект модели
                elif not isinstance(value, int):  # Проверяем, что значение — число
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")

            fields.append(f'"{field_name}"')
            
            # Форматируем значение для SQL
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        # Формируем SQL-запрос с встроенными значениями
        insert_query = f'INSERT INTO "{self.model_class.get_table_name()}" ({", ".join(fields)}) VALUES ({", ".join(values)})'
        db.execute(insert_query)

        # Получаем ID созданной записи
        last_id = db.lastrowid()
        if last_id is None:
            raise RuntimeError("Failed to retrieve the ID of the newly created record.")
        return self.model_class.objects.get(id=last_id)

    def save(self, instance):
        data = instance.__dict__

        if hasattr(instance, 'id') and instance.id is not None:
            # UPDATE
            set_clauses = []
            for key, value in data.items():
                if key != 'id':
                    if isinstance(value, str):
                        set_clauses.append(f'"{key}"=\'{value}\'')
                    else:
                        set_clauses.append(f'"{key}"={value}')
            
            update_query = f'UPDATE "{self.model_class.get_table_name()}" SET {", ".join(set_clauses)} WHERE id={instance.id}'
            db.execute(update_query)
        else:
            # INSERT
            fields = []
            values = []
            for key, value in data.items():
                if key != 'id':
                    fields.append(f'"{key}"')
                    if isinstance(value, str):
                        values.append(f"'{value}'")
                    else:
                        values.append(str(value))

            insert_query = f'INSERT INTO "{self.model_class.get_table_name()}" ({", ".join(fields)}) VALUES ({", ".join(values)})'
            db.execute(insert_query)

            last_id = db.lastrowid()
            if last_id is None:
                raise RuntimeError("Failed to retrieve the ID of the newly created record.")
            instance.id = last_id

        return instance
    
    def __getitem__(self, key):
        """
        Обрабатывает срезы (например, [:10]).
        """
        if isinstance(key, slice):
            # Если start не указан, используем 0
            limit = key.stop - (key.start or 0)
            offset = key.start or 0

            new_queryset = QuerySet(self.model_class)
            new_queryset.query = self.query
            new_queryset.params = self.params

            if limit is not None:
                new_queryset.query += f" LIMIT {limit}"
            if offset:
                new_queryset.query += f" OFFSET {offset}"

            return new_queryset.execute()

        raise TypeError("QuerySet indices must be slices")
    
    def __iter__(self):
        """
        Делает QuerySet итерируемым, выполняя запрос при необходимости.
        """
        return iter(self.execute())

    def count(self):
        """
        Возвращает количество записей в QuerySet.
        """
        # Заменяем SELECT * на SELECT COUNT(*)
        count_query = self.query.replace('SELECT *', 'SELECT COUNT(*)')
        result = db.execute(count_query, self.params or (), fetch=True)
        return result[0][0] if result else 0

    def exists(self):
        """
        Проверяет, существуют ли записи в QuerySet.
        """
        return self.count() > 0

    def delete(self):
        """
        Удаляет все записи в QuerySet.
        """
        # Создаем DELETE запрос
        delete_query = f'DELETE FROM "{self.model_class.get_table_name()}"'
        
        # Добавляем WHERE условия если они есть
        if 'WHERE' in self.query:
            where_clause = self.query.split('WHERE')[1]
            delete_query += f" WHERE {where_clause}"
        
        db.execute(delete_query, self.params or ())
        return True
    
    # Асинхронные методы
    async def filter_async(self, **kwargs):
        """
        Асинхронная версия filter.
        """
        # Create new QuerySet for query chaining
        new_queryset = QuerySet(self.model_class)
        conditions = []

        for field_name, value in kwargs.items():
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")

            field = self.model_class._fields[field_name]

            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id  # Extract id if model object is passed
                elif not isinstance(value, int):
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")

            # Вставляем значение напрямую в запрос для SQLAlchemy
            if isinstance(value, str):
                conditions.append(f'"{field_name}"=\'{value}\'')
            else:
                conditions.append(f'"{field_name}"={value}')

        # Form new query with conditions
        new_queryset.query = f"{self.query} WHERE {' AND '.join(conditions)}"
        new_queryset.params = None  # Не используем параметры для SQLAlchemy
        return new_queryset
    
    async def all_async(self):
        """
        Асинхронная версия all.
        """
        return self
    
    async def first_async(self):
        """
        Асинхронная версия first.
        """
        # Add LIMIT 1 to current query
        query = f"{self.query} LIMIT 1"
        result = await db.execute_async(query, self.params or (), fetch=True)

        if result:
            row = result[0]
            return self.model_class(**{
                key: value for key, value in zip(self.model_class._fields.keys(), row)
                if key in self.model_class._fields
            })
        return None
    
    async def order_by_async(self, *fields):
        """
        Асинхронная версия order_by.
        """
        new_queryset = QuerySet(self.model_class)
        new_queryset.query = self.query
        new_queryset.params = self.params
        new_queryset.order_by_fields = list(fields)  # Save sorting fields

        # Add ORDER BY to query
        order_conditions = []
        for field in fields:
            if field.startswith('-'):
                # Descending sort
                order_conditions.append(f'"{field[1:]}" DESC')
            else:
                # Ascending sort
                order_conditions.append(f'"{field}" ASC')

        if order_conditions:
            new_queryset.query += f" ORDER BY {', '.join(order_conditions)}"

        return new_queryset
    
    async def execute_async(self):
        """
        Асинхронная версия execute.
        """
        # Execute current query and return result
        result = await db.execute_async(self.query, self.params or (), fetch=True)
        return [
            self.model_class(**dict(zip(self.model_class._fields.keys(), row)))
            for row in result
        ]
    
    async def create_async(self, **kwargs):
        """
        Асинхронная версия create.
        """
        fields = []
        values = []

        for field_name, value in kwargs.items():
            # Проверяем, существует ли поле в текущей модели
            if field_name not in self.model_class._fields:
                raise KeyError(f"Field '{field_name}' does not exist in model '{self.model_class.__name__}'")

            field = self.model_class._fields[field_name]

            # Обработка внешних ключей
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                if related_model and isinstance(value, related_model):
                    value = value.id  # Извлекаем id, если передан объект модели
                elif not isinstance(value, int):  # Проверяем, что значение — число
                    raise ValueError(f"Invalid value for foreign key '{field_name}': {value}")

            fields.append(f'"{field_name}"')
            
            # Форматируем значение для SQL
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        # Формируем SQL-запрос с встроенными значениями
        insert_query = f'INSERT INTO "{self.model_class.get_table_name()}" ({", ".join(fields)}) VALUES ({", ".join(values)})'
        await db.execute_async(insert_query)

        # Получаем ID созданной записи
        last_id = await db.lastrowid_async()
        if last_id is None:
            raise RuntimeError("Failed to retrieve the ID of the newly created record.")
        return await self.model_class.objects.get_async(id=last_id)
    
    async def save_async(self, instance):
        """
        Асинхронная версия save.
        """
        data = instance.__dict__

        if hasattr(instance, 'id') and instance.id is not None:
            # UPDATE
            set_clauses = []
            for key, value in data.items():
                if key != 'id':
                    if isinstance(value, str):
                        set_clauses.append(f'"{key}"=\'{value}\'')
                    else:
                        set_clauses.append(f'"{key}"={value}')
            
            update_query = f'UPDATE "{self.model_class.get_table_name()}" SET {", ".join(set_clauses)} WHERE id={instance.id}'
            await db.execute_async(update_query)
        else:
            # INSERT
            fields = []
            values = []
            for key, value in data.items():
                if key != 'id':
                    fields.append(f'"{key}"')
                    if isinstance(value, str):
                        values.append(f"'{value}'")
                    else:
                        values.append(str(value))

            insert_query = f'INSERT INTO "{self.model_class.get_table_name()}" ({", ".join(fields)}) VALUES ({", ".join(values)})'
            await db.execute_async(insert_query)

            last_id = await db.lastrowid_async()
            if last_id is None:
                raise RuntimeError("Failed to retrieve the ID of the newly created record.")
            instance.id = last_id

        return instance
    
    async def count_async(self):
        """
        Асинхронная версия count.
        """
        count_query = self.query.replace('SELECT *', 'SELECT COUNT(*)')
        result = await db.execute_async(count_query, self.params or (), fetch=True)
        return result[0][0] if result else 0
    
    async def exists_async(self):
        """
        Асинхронная версия exists.
        """
        return await self.count_async() > 0
    
    async def delete_async(self):
        """
        Асинхронная версия delete.
        """
        delete_query = f'DELETE FROM "{self.model_class.get_table_name()}"'
        
        # Добавляем WHERE условия если они есть
        if 'WHERE' in self.query:
            where_clause = self.query.split('WHERE')[1]
            delete_query += f" WHERE {where_clause}"
        
        await db.execute_async(delete_query, self.params or ())
        return True
