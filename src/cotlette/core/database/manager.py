import asyncio
from cotlette.core.database.query import QuerySet, is_async_context

class Manager:
    def __init__(self, model_class):
        self.model_class = model_class

    def filter(self, **kwargs):
        return QuerySet(self.model_class).filter(**kwargs)

    def all(self):
        return QuerySet(self.model_class).all()

    def create(self, **kwargs):
        # create обычно сразу создает объект, поэтому реализуем sync+async
        if is_async_context():
            return QuerySet(self.model_class)._create_async(**kwargs)
        else:
            return QuerySet(self.model_class)._create_sync(**kwargs)

    def get(self, **kwargs):
        # get = filter + first
        qs = QuerySet(self.model_class).filter(**kwargs)
        return qs.first()

    def count(self):
        return QuerySet(self.model_class).count()

    def exists(self):
        return QuerySet(self.model_class).exists()

    def delete(self, **kwargs):
        qs = QuerySet(self.model_class).filter(**kwargs)
        return qs.delete()
