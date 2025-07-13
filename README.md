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
- **Asynchronous Support**: Full async views and endpoints
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

## Example: Creating a View
```python
from fastapi import APIRouter
from cotlette.shortcuts import render_template
from .models import Article

router = APIRouter()

@router.get("/")
async def home():
    articles = Article.objects.all().execute()
    return render_template("index.html", {"articles": articles})
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
