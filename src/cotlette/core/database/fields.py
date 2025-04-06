class Field:
    def __init__(self, column_type, primary_key=False, default=None, unique=False):
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.unique = unique  # Добавляем поддержку параметра unique

class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class AutoField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", primary_key=True, **kwargs)

class ForeignKeyField(Field):
    def __init__(self, to, related_name=None, **kwargs):
        """
        :param to: Связанная модель (класс или строка с именем модели).
        :param related_name: Имя обратной связи (опционально).
        :param kwargs: Дополнительные параметры.
        """
        super().__init__("INTEGER", **kwargs)
        self.to = to  # Связанная модель
        self.related_name = related_name  # Имя для обратной связи

    def contribute_to_class(self, model_class, name):
        """
        Метод, который связывает поле с моделью.
        :param model_class: Класс модели, к которой добавляется поле.
        :param name: Имя поля в модели.
        """
        self.name = name
        self.model_class = model_class

        # Добавляем поле в список полей модели
        if not hasattr(model_class, '_meta'):
            model_class._meta = {}
        if 'foreign_keys' not in model_class._meta:
            model_class._meta['foreign_keys'] = []
        model_class._meta['foreign_keys'].append(self)

    # def get_related_model(self):
    #     """
    #     Возвращает связанную модель.
    #     Если self.to — строка, то ищет модель по имени.
    #     """
    #     if isinstance(self.to, str):
    #         # Предполагается, что модели доступны в глобальном пространстве имён
    #         return globals()[self.to]
    #     return self.to

    def get_related_model(self):
        """
        Возвращает связанную модель.
        Если self.to — строка, то ищет модель в реестре.
        """
        from cotlette.core.database.models import ModelMeta
        if isinstance(self.to, str):
            return ModelMeta.get_model(self.to)
        return self.to