# Cotlette Technical Documentation

## Overview

Cotlette is a modern, Django-inspired web framework built on top of FastAPI. It provides a familiar project structure, its own ORM, template rendering, and a set of management commands for rapid web development. Cotlette is designed for both beginners and advanced users who want the power of FastAPI with the convenience of Django-like tools.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Request Lifecycle](#request-lifecycle)
- [ORM](#orm)
- [Templates](#templates)
- [Middleware](#middleware)
- [Management Commands](#management-commands)
- [Extending Cotlette](#extending-cotlette)
- [FAQ](#faq)

---

## Project Structure

A typical Cotlette project looks like this:

```
myproject/
├── apps/
│   ├── users/
│   └── blog/
├── config/
│   ├── settings.py
│   └── urls.py
├── core/
│   └── __init__.py
├── manage.py
├── templates/
│   └── ...
└── static/
```

- **apps/**: Your Django-style applications (users, blog, etc.)
- **config/**: Project settings and URL configuration
- **core/**: Project core logic (optional)
- **manage.py**: Command-line utility
- **templates/**: Jinja2 templates
- **static/**: Static files (CSS, JS, images)

---

## Architecture

Cotlette is built on FastAPI and leverages its async capabilities. Key components:

- **ASGI app**: FastAPI-based, with Cotlette-specific extensions
- **ORM**: Synchronous, inspired by Django ORM, supports SQLite (PostgreSQL in roadmap)
- **Template Engine**: Jinja2 integration
- **Management Commands**: CLI for project/app creation, server, shell, migrations (planned)
- **Admin Panel**: Built-in, customizable

---

## Request Lifecycle

1. **Request** comes in via ASGI (Uvicorn/Hypercorn)
2. **Middleware** (authentication, sessions, etc.)
3. **Router** dispatches to the correct view
4. **View** processes request, interacts with ORM, renders template or returns JSON
5. **Response** is sent back to the client

---

## ORM

- **Models**: Define models using Python classes and field types
- **CRUD**: Create, retrieve, update, delete records
- **QuerySet**: Chainable queries, filtering, ordering
- **Relationships**: ForeignKey, OneToOne, ManyToMany (in progress)
- **Migrations**: Planned for future releases

See [.docs/orm.md](./orm.md) for details and examples.

---

## Templates

- **Jinja2**: Full support for Jinja2 templates
- **Template context**: Pass variables from views
- **Custom filters/tags**: Easily extendable

See [.docs/templates.md](./templates.md) for usage.

---

## Middleware

- **Built-in**: Authentication, session, CSRF (planned)
- **Custom**: Write your own middleware for request/response processing

See [.docs/middleware.md](./middleware.md).

---

## Management Commands

- `startproject`, `startapp`, `runserver`, `shell`, `makemigrations` (planned), `migrate` (planned)
- Extensible command system

See [.docs/commands.md](./commands.md).

---

## Extending Cotlette

- **Custom apps**: Add your own Django-style apps
- **Custom commands**: Add CLI commands
- **Custom middleware**: Plug into the request lifecycle

See [.docs/extending.md](./extending.md).

---

## FAQ

See [.docs/faq.md](./faq.md) for common questions and troubleshooting.

---

## More

- [ORM Reference](./orm.md)
- [Template Reference](./templates.md)
- [Command Reference](./commands.md)
- [Middleware Reference](./middleware.md)
- [Extending Cotlette](./extending.md)
- [FAQ](./faq.md) 