# Raystack Management Commands

## Overview

Raystack provides a set of command-line tools for project management, similar to Django's `manage.py` or Flask CLI. These commands help you create projects, apps, run the development server, and more.

---

## Available Commands

### `startproject <project_name>`
Creates a new Raystack project with the recommended structure.

```
raystack startproject myproject
```

### `startapp <app_name>`
Creates a new app inside your project.

```
raystack startapp blog
```

### `runserver`
Starts the development server (default: http://127.0.0.1:8000).

```
raystack runserver
```

### `shell`
Launches an interactive Python shell with project context loaded.

```
raystack shell
```

### `createsuperuser`
Creates a superuser account with all permissions.

```
raystack createsuperuser
```

Options:
- `--username`: Specify username (optional)
- `--email`: Specify email address (optional)
- `--noinput`: Create without prompting for input

Examples:
```bash
# Interactive creation
raystack createsuperuser

# Non-interactive creation
raystack createsuperuser --username admin --email admin@example.com --noinput
```

### `makemigrations` *(planned)*
Generates migration files for model changes.

### `migrate` *(planned)*
Applies migrations to the database.

---

## Custom Commands

You can add your own management commands by creating a Python module in `raystack/core/management/commands/`.

Example:
```python
# myproject/core/management/commands/hello.py
from raystack.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Prints Hello, World!"

    def handle(self, *args, **options):
        print("Hello, World!")
```

Run with:
```
raystack hello
```

---

## Command Reference

- All commands support `--help` for usage info:

```
raystack runserver --help
```

---

## Best Practices

- Use `startproject` and `startapp` to scaffold new code
- Keep custom commands in `core/management/commands/`
- Use the shell for quick database and model testing
- Use `createsuperuser` to create admin accounts

---

## Roadmap

- Database migrations
- Command auto-discovery
- Interactive admin commands 