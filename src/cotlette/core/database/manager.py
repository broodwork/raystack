from cotlette.core.database.query import QuerySet

class Manager:
    def __init__(self, model_class):
        self.model_class = model_class

    def filter(self, **kwargs):
        return QuerySet(self.model_class).filter(**kwargs)

    def all(self):
        return QuerySet(self.model_class).all()

    def create(self, **kwargs):
        """
        Создает новую запись в базе данных.
        :param kwargs: Значения полей для новой записи.
        :return: Созданный экземпляр модели.
        """
        return QuerySet(self.model_class).create(**kwargs)

    def get(self, **kwargs):
        """
        Получает одну запись из базы данных по заданным параметрам.
        :param kwargs: Параметры для фильтрации.
        :return: Экземпляр модели или None.
        """
        return QuerySet(self.model_class).filter(**kwargs).first()

    def count(self):
        """
        Возвращает количество записей в модели.
        """
        return QuerySet(self.model_class).count()

    def exists(self):
        """
        Проверяет, существуют ли записи в модели.
        """
        return QuerySet(self.model_class).exists()

    def delete(self, **kwargs):
        """
        Удаляет записи из базы данных.
        :param kwargs: Параметры для фильтрации.
        :return: True если удаление прошло успешно.
        """
        return QuerySet(self.model_class).filter(**kwargs).delete()
    
    # Асинхронные методы
    async def filter_async(self, **kwargs):
        """
        Асинхронная версия filter.
        """
        return await QuerySet(self.model_class).filter_async(**kwargs)
    
    async def all_async(self):
        """
        Асинхронная версия all.
        """
        return await QuerySet(self.model_class).all_async()
    
    async def create_async(self, **kwargs):
        """
        Асинхронно создает новую запись в базе данных.
        :param kwargs: Значения полей для новой записи.
        :return: Созданный экземпляр модели.
        """
        return await QuerySet(self.model_class).create_async(**kwargs)
    
    async def get_async(self, **kwargs):
        """
        Асинхронно получает одну запись из базы данных по заданным параметрам.
        :param kwargs: Параметры для фильтрации.
        :return: Экземпляр модели или None.
        """
        queryset = await QuerySet(self.model_class).filter_async(**kwargs)
        return await queryset.first_async()
    
    async def count_async(self):
        """
        Асинхронная версия count.
        """
        return await QuerySet(self.model_class).count_async()
    
    async def exists_async(self):
        """
        Асинхронная версия exists.
        """
        return await QuerySet(self.model_class).exists_async()
    
    async def delete_async(self, **kwargs):
        """
        Асинхронно удаляет записи из базы данных.
        :param kwargs: Параметры для фильтрации.
        :return: True если удаление прошло успешно.
        """
        queryset = await QuerySet(self.model_class).filter_async(**kwargs)
        return await queryset.delete_async()
