from cotlette.core.database.fields import CharField, IntegerField, Field
from cotlette.core.database.manager import Manager
from cotlette.core.database.backends.sqlite3 import db
from cotlette.core.database.fields.related import ForeignKeyField

from cotlette.core.database.fields import AutoField


class ModelMeta(type):
    _registry = {}  # Dictionary for storing registered models

    def __new__(cls, name, bases, attrs):
        # Create new class
        new_class = super().__new__(cls, name, bases, attrs)

        # Register model in registry if it's not the base Model class
        if name != "Model":
            cls._registry[name] = new_class

        # Collect fields in _fields dictionary
        fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):  # Check if attribute is Field instance
                attr_value.contribute_to_class(new_class, attr_name)  # Call contribute_to_class
                fields[attr_name] = attr_value

        # Attach _fields to class
        new_class._fields = fields
        return new_class

    @classmethod
    def get_model(cls, name):
        """
        Returns model by name from registry.
        """
        return cls._registry.get(name)


class Model(metaclass=ModelMeta):
    table = None

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.objects = Manager(cls)
        cls.objects.model_class = cls
    
    def __getattr__(self, name):
        """
        Dynamic access to object attributes.
        If attribute doesn't exist, AttributeError is raised.
        """
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"'{self.get_table_name()}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Dynamic setting of attribute values.
        """
        self.__dict__[name] = value
    
    def __str__(self):
        return "<%s object (%s)>" % (self.get_table_name(), self.id)

    def to_dict(self, exclude_private=True):
        """
        Convert model object to dictionary.
        :param exclude_private: If True, private fields won't be added to dictionary.
        """
        return {
            key: getattr(self, key)
            for key in self.__dict__
            if (not key.startswith("_") or not exclude_private)
        }

    @classmethod
    def get_table_name(cls):
        return (
            cls.table 
            if hasattr(cls, "table") and cls.table 
            else "_".join(cls.__module__.split('.')[1:-1] + [cls.__name__.lower()])
        )

    @classmethod
    def create_table(cls):
        # TODO: Move to database.backends... specifically for SQLite3 and future PostgreSQL

        columns = []
        foreign_keys = []

        for field_name, field in cls._fields.items():
            # Form column definition
            column_def = f'"{field_name}" {field.column_type}'
            
            # Add autoincrement for primary key
            if isinstance(field, AutoField):  # Check if field is autoincrement
                column_def += " PRIMARY KEY AUTOINCREMENT"  # For SQLite
                # If PostgreSQL is used, make it "SERIAL PRIMARY KEY"
            elif field.primary_key:
                column_def += " PRIMARY KEY"
            
            if field.unique:
                column_def += " UNIQUE"
            columns.append(column_def)

            # Check if field is foreign key
            if isinstance(field, ForeignKeyField):
                related_model = field.get_related_model()
                foreign_keys.append(
                    f'FOREIGN KEY ("{field_name}") REFERENCES "{related_model.table or related_model.__name__}"("id")'
                )

        # Combine columns and foreign keys into one list
        all_parts = columns + foreign_keys

        # Form final SQL query
        query = f'CREATE TABLE IF NOT EXISTS "{cls.get_table_name()}" ({", ".join(all_parts)});'

        db.execute(query)  # Execute table creation query
        db.commit()        # Commit changes

    def save(self):
        """
        Saves current object to database.
        If object already exists (has id), UPDATE is performed.
        If object is new (id is missing or None), INSERT is performed.
        """
        # Get field values from object
        data = {field: getattr(self, field, None) for field in self._fields}

        # Convert values to supported SQLite types
        def convert_value(value):
            if isinstance(value, (int, float, str, bytes, type(None))):
                return value
            elif hasattr(value, '__str__'):
                return str(value)  # Convert object to string if possible
            else:
                raise ValueError(f"Unsupported type for database: {type(value)}")

        data = {key: convert_value(value) for key, value in data.items()}

        # Check if object exists in database
        if hasattr(self, 'id') and self.id is not None:
            # Update existing record (UPDATE)
            fields = ', '.join([f"{key}=?" for key in data if key != 'id'])
            values = tuple(data[key] for key in data if key != 'id') + (self.id,)
            update_query = f"UPDATE {self.get_table_name()} SET {fields} WHERE id=?"
            db.execute(update_query, values)
            db.commit()
        else:
            # Create new record (INSERT)
            fields = ', '.join([key for key in data if key != 'id'])
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data[key] for key in data if key != 'id')

            insert_query = f"INSERT INTO {self.get_table_name()} ({fields}) VALUES ({placeholders})"
            db.execute(insert_query, values)
            db.commit()

            # Get id of created record
            self.id = db.lastrowid
