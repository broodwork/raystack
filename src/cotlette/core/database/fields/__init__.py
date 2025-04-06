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
