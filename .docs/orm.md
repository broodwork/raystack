# Raystack ORM Documentation

## Overview

Raystack includes a lightweight, Django-inspired ORM for working with relational databases (currently SQLite, PostgreSQL in roadmap). It provides a familiar API for defining models, querying data, and managing relationships.

---

## Defining Models

Models are Python classes that inherit from `raystack.db.Model` and use field types from `raystack.db.fields`:

```python
from raystack.db import Model, fields

class Article(Model):
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    published_at = fields.DateTimeField(auto_now_add=True)
```

### Field Types
- `CharField(max_length)`
- `TextField()`
- `IntegerField()`
- `BooleanField()`
- `DateTimeField()`
- `ForeignKey(to)`

---

## CRUD Operations

### Create
```python
article = await Article.objects.create(title="Hello", content="Text")
```

### Retrieve
```python
all_articles = await Article.objects.all()
article = await Article.objects.filter(id=1).first()
```

### Update
```python
article.title = "New Title"
await article.save()
```

### Delete
```python
await article.delete()
```

---

## QuerySet API

- `.all()` — get all records
- `.filter(**kwargs)` — filter by fields
- `.exclude(**kwargs)` — exclude by fields (planned)
- `.order_by('field', '-field')` — ordering
- `.first()` — first result
- `.last()` — last result (planned)
- `.count()` — count results (planned)

---

## Relationships

- `ForeignKey` — many-to-one
- `OneToOneField` — one-to-one (planned)
- `ManyToManyField` — many-to-many (planned)

Example:
```python
class Author(Model):
    name = fields.CharField(max_length=100)

class Book(Model):
    title = fields.CharField(max_length=200)
    author = fields.ForeignKey(Author)
```

---

## Migrations

*Automatic migrations are not yet implemented. You must manually create tables using `Model.create_table()`.*

```python
Article.create_table()
```

---

## Advanced Usage

- **Custom methods**: Add your own methods to models
- **Meta options**: Use `class Meta` for table name, ordering, etc. (planned)
- **Raw SQL**: Use `Model.objects.raw(sql)` for custom queries (planned)

---

## Limitations

- Only SQLite is fully supported (PostgreSQL in progress)
- No migrations yet (manual table creation)
- No advanced lookups (e.g., `icontains`, `gte`, etc.)
- No signals, hooks, or advanced validation

---

## Examples

See the [examples](../example/) directory for real-world usage.

---

## Roadmap

- PostgreSQL support
- Migrations
- Advanced query lookups
- Aggregations
- Signals/hooks
- Admin integration 