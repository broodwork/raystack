class Field:
    def __init__(self, column_type, primary_key=False, default=None):
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class AutoField(Field):
    def __init__(self, **kwargs):
        # Устанавливаем тип поля как INTEGER и делаем его первичным ключом
        # super().__init__("INTEGER", primary_key=True, **kwargs)
        super().__init__("INTEGER", **kwargs)