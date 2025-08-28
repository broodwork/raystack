# Raystack Templates Documentation

## Overview

Raystack uses Jinja2 as its template engine, providing a familiar and powerful way to render HTML pages with dynamic content.

---

## Template Directory Structure

By default, templates are stored in the `templates/` directory at the project root or inside each app:

```
myproject/
├── templates/
│   ├── base.html
│   └── index.html
└── apps/
    └── blog/
        └── templates/
            └── blog/
                └── post_detail.html
```

---

## Rendering Templates

Use the `render_template` shortcut in your views:

```python
from raystack.shortcuts import render_template

@router.get("/")
async def home():
    return render_template("index.html", {"key": "value"})
```

---

## Template Context

Pass variables to templates as a dictionary:

```python
return render_template("profile.html", {"user": user, "posts": posts})
```

In the template:
```jinja2
<h1>Hello, {{ user.username }}!</h1>
<ul>
  {% for post in posts %}
    <li>{{ post.title }}</li>
  {% endfor %}
</ul>
```

---

## Extending Templates

Use Jinja2's `{% extends %}` and `{% block %}` for layout inheritance:

```jinja2
<!-- base.html -->
<html>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>
```

```jinja2
<!-- index.html -->
{% extends "base.html" %}
{% block content %}
  <h1>Welcome!</h1>
{% endblock %}
```

---

## Custom Filters and Tags

You can register custom Jinja2 filters and global functions in your project:

```python
def reverse_string(value):
    return value[::-1]

app.jinja_env.filters['reverse'] = reverse_string
```

Usage in template:
```jinja2
{{ 'raystack'|reverse }}
```

---

## Static Files

Use the `{% static %}` tag to refer to static files (if enabled):

```jinja2
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

---

## Template Settings

Configure template directories and options in `config/settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "raystack.template.backends.jinja2.Jinja2",
        "DIRS": ["templates"],
        "APP_DIRS": True,
    },
]
```

---

## Best Practices

- Use base templates for layout
- Keep logic out of templates (use context)
- Organize templates by app for large projects

---

## More

See [Jinja2 documentation](https://jinja.palletsprojects.com/) for advanced features. 