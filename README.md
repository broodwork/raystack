![PyPI Version](https://img.shields.io/pypi/v/cotlette)
![Python Versions](https://img.shields.io/pypi/pyversions/cotlette)
![License](https://img.shields.io/pypi/l/cotlette)
![Downloads](https://img.shields.io/pypi/dm/cotlette)

# Cotlette 🚀

**Cotlette** is a modern, Django-inspired web framework built on top of **FastAPI**. It combines the best of both worlds: the speed and async power of FastAPI with the convenience of Django-like project structure, ORM, templates, and management commands.

---

## Key Features

- **FastAPI Under the Hood**: High-performance async web framework
- **Django-like Project Structure**: Familiar and easy to organize
- **SQLAlchemy-powered ORM**: Simple, Pythonic, and extensible with support for multiple databases
- **Alembic Migrations**: Powerful database migration system
- **Jinja2 Templates**: Powerful and flexible HTML rendering
- **Admin Panel**: Built-in, customizable (inspired by Django admin)
- **Management Commands**: CLI for project/app creation, server, shell, migrations, and more
- **Asynchronous Support**: Full async views and endpoints with automatic context detection
- **Multi-Database Support**: SQLite, PostgreSQL, MySQL, Oracle, and more
- **Extensible**: Add your own apps, middleware, commands, and more

---

## Quick Start

### 1. Install Cotlette
```bash
pip install cotlette
```

### 2. Create a New Project
```bash
cotlette startproject myproject
cd myproject
```

### 3. Run the Development Server
```bash
cotlette runserver
```

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000/)

---

## Screenshots

**Home Page:**
![Home Page](.docs/img/first_page.jpg)

**Login Page:**
![Login Page](.docs/img/login_page.jpg)

**Admin Panel:**
![Admin Page](.docs/img/admin_page.jpg)

---

## Example: Defining a Model
```python
from cotlette.core.database import Model, CharField, IntegerField, AutoField

class Article(Model):
    id = AutoField(primary_key=True)
    title = CharField(max_length=200)
    content = CharField(max_length=1000)
    author_id = IntegerField()
```

---

## Universal ORM Usage

Cotlette ORM automatically detects whether you're in a synchronous or asynchronous context and works accordingly. No need for separate sync/async methods!

### Basic CRUD Operations
```python
# Create
article = Article.objects.create(title="Hello", content="World", author_id=1)

# Get
article = Article.objects.get(id=1)

# Filter
articles = Article.objects.filter(author_id=1).execute()

# Update
article.title = "Updated Title"
article.save()

# Delete
article.delete()

# Count
count = Article.objects.count()

# Exists
exists = Article.objects.exists()
```

### In Async Context
When used in async functions, the same methods automatically work asynchronously:

```python
async def async_view():
    # Create
    article = await Article.objects.create(title="Hello", content="World", author_id=1)
    
    # Get
    article = await Article.objects.get(id=1)
    
    # Filter
    articles = await Article.objects.filter(author_id=1).execute()
    
    # Update
    article.title = "Updated Title"
    await article.save()
    
    # Delete
    await article.delete()
    
    # Count
    count = await Article.objects.count()
    
    # Exists
    exists = await Article.objects.exists()
```

---

## Example: Creating Views

### Synchronous View
```python
from fastapi import APIRouter
from cotlette.shortcuts import render_template
from .models import Article

router = APIRouter()

@router.get("/sync")
def home():
    articles = Article.objects.all().execute()
    return render_template("index.html", {"articles": articles})
```

### Asynchronous View
```python
from fastapi import APIRouter
from cotlette.shortcuts import render_template
from .models import Article

router = APIRouter()

@router.get("/async")
async def home():
    articles = await Article.objects.all().execute()
    return render_template("index.html", {"articles": articles})
```

**Note**: The same ORM methods work in both contexts! Cotlette automatically detects the execution context.

---

## Advanced ORM Features

### Query Chaining
```python
# Complex queries with chaining
articles = Article.objects.filter(author_id=1).order_by('-id').execute()

# In async context
articles = await Article.objects.filter(author_id=1).order_by('-id').execute()
```

### Bulk Operations
```python
# Create multiple objects
articles = [
    Article(title="Article 1", content="Content 1", author_id=1),
    Article(title="Article 2", content="Content 2", author_id=1),
]

for article in articles:
    article.save()

# In async context
for article in articles:
    await article.save()
```

### Database Support
Cotlette supports multiple databases through SQLAlchemy:

```python
# SQLite (default)
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite:///db.sqlite3',
    }
}

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'postgresql://user:pass@localhost/dbname',
    }
}

# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'mysql://user:pass@localhost/dbname',
    }
}
```

---

## Management Commands

### Project Management
- `cotlette startproject <project_name>` — Create a new Cotlette project directory structure
- `cotlette startapp <app_name>` — Create a new Cotlette app directory structure

### Development Server
- `cotlette runserver [addrport]` — Start the development server
  - Optional arguments: `--ipv6`, `--reload`
  - Example: `cotlette runserver 0.0.0.0:8000`

### Interactive Shell
- `cotlette shell` — Interactive Python shell with auto-imports
  - Options: `--no-startup`, `--no-imports`, `--interface`, `--command`
  - Supports IPython, bpython, and standard Python

### Database Management
- `cotlette makemigrations [--message] [--empty]` — Create database migrations
  - Options: `--message`, `--empty`
  - Example: `cotlette makemigrations --message "Add user model"`
- `cotlette migrate [--revision] [--fake]` — Apply database migrations
  - Options: `--revision`, `--fake`
  - Example: `cotlette migrate --revision head`

### User Management
- `cotlette createsuperuser` — Create a superuser account
  - Options: `--username`, `--email`, `--noinput`
  - Interactive mode for secure password input

---

## Documentation

- [Technical Documentation](.docs/index.md)
- [ORM Reference](.docs/orm.md)
- [Template Reference](.docs/templates.md)
- [Command Reference](.docs/commands.md)
- [Middleware Reference](.docs/middleware.md)
- [Extending Cotlette](.docs/extending.md)
- [FAQ](.docs/faq.md)

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests and issues are welcome! See [GitHub](https://github.com/ForceFledgling/cotlette).
