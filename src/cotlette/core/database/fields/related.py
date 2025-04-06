from cotlette.core.database.fields import Field
from cotlette.core.exceptions import ValidationError

class ForeignKeyField(Field):
    """
    Поле для создания внешнего ключа между моделями.
    """

    def __init__(self, to, on_delete=None, related_name=None, to_field=None, **kwargs):
        """
        :param to: Связанная модель (класс или строка с именем модели).
        :param on_delete: Функция, которая определяет поведение при удалении связанного объекта.
        :param related_name: Имя обратной связи (опционально).
        :param to_field: Поле в связанной модели, которое используется для связи (по умолчанию PK).
        :param kwargs: Дополнительные параметры.
        """
        super().__init__("INTEGER", **kwargs)
        self.to = to  # Связанная модель
        self.on_delete = on_delete  # Поведение при удалении
        self.related_name = related_name  # Имя для обратной связи
        self.to_field = to_field  # Поле в связанной модели

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

        # Добавляем обратную связь в связанную модель
        related_model = self.get_related_model()
        if self.related_name and hasattr(related_model, '_meta'):
            if 'reverse_relations' not in related_model._meta:
                related_model._meta['reverse_relations'] = {}
            related_model._meta['reverse_relations'][self.related_name] = model_class

    def get_related_model(self):
        """
        Возвращает связанную модель.
        Если self.to — строка, то ищет модель в реестре.
        """
        from cotlette.core.database.models import ModelMeta
        if isinstance(self.to, str):
            try:
                return ModelMeta.get_model(self.to)
            except KeyError:
                raise ValueError(f"Related model '{self.to}' is not registered in ModelMeta.")
        return self.to

    def validate(self, value):
        """
        Валидация значения внешнего ключа.
        """
        related_model = self.get_related_model()
        if value is None:
            return  # Допустимо, если поле необязательное
        if not isinstance(value, related_model):
            raise ValidationError(f"Value must be an instance of {related_model.__name__}.")