# Extending Raystack

## Overview

Raystack is designed to be extensible. You can add your own apps, commands, middleware, and even swap out core components. This guide covers the main extension points.

---

## Custom Apps

Add Django-style apps to the `apps/` directory. Each app can have its own models, views, templates, and static files.

Example structure:
```
apps/
  blog/
    __init__.py
    models.py
    views.py
    templates/
    static/
```

Register your app in `INSTALLED_APPS` in `config/settings.py`:
```python
INSTALLED_APPS = [
    "apps.blog",
]
```

---

## Custom Management Commands

Add Python modules to `core/management/commands/`:
```python
# core/management/commands/hello.py
from raystack.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Prints Hello, World!"
    def handle(self, *args, **options):
        print("Hello, World!")
```

---

## Custom Middleware

Write your own middleware and add it to the app:
```python
from raystack.core.middlewares import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def __call__(self, request, call_next):
        # Do something with request
        response = await call_next(request)
        # Do something with response
        return response

app.add_middleware(MyMiddleware)
```

---

## Custom Template Filters

Register custom Jinja2 filters:
```python
def shout(value):
    return value.upper() + "!"

app.jinja_env.filters['shout'] = shout
```

---

## Swapping Components

You can override or extend core components (ORM, template engine, etc.) by subclassing and registering your own implementations.

---

## Best Practices

- Keep apps modular and reusable
- Use management commands for automation
- Write middleware for cross-cutting concerns
- Document your extensions

---

## More

See the [Raystack source code](../src/raystack/) for more extension examples. 