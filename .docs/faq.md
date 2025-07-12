# Cotlette FAQ

## General

**Q: What is Cotlette?**  
A: Cotlette is a modern web framework inspired by Django and built on top of FastAPI. It provides a familiar project structure, its own ORM, template rendering, and management commands.

**Q: What Python versions are supported?**  
A: Python 3.6 and higher.

**Q: What databases are supported?**  
A: SQLite is fully supported. PostgreSQL support is planned.

---

## Installation

**Q: How do I install Cotlette?**  
A: Run `pip install cotlette`.

**Q: How do I create a new project?**  
A: Run `cotlette startproject myproject`.

---

## Development

**Q: How do I run the development server?**  
A: Run `cotlette runserver` in your project directory.

**Q: How do I create a new app?**  
A: Run `cotlette startapp myapp`.

**Q: How do I use the shell?**  
A: Run `cotlette shell` for an interactive Python shell with project context.

---

## ORM

**Q: How do I define a model?**  
A: Inherit from `cotlette.db.Model` and use field types from `cotlette.db.fields`.

**Q: How do I create tables?**  
A: Call `Model.create_table()` for each model.

**Q: Are migrations supported?**  
A: Not yet. Manual table creation is required.

---

## Templates

**Q: What template engine is used?**  
A: Jinja2.

**Q: How do I render a template?**  
A: Use `render_template("template.html", context)` in your view.

---

## Troubleshooting

**Q: I get `ModuleNotFoundError: No module named 'cotlette'`**  
A: Make sure your `PYTHONPATH` includes the `src/` directory, or install Cotlette in your environment.

**Q: The server runs but I see a 404 page**  
A: Make sure you have defined routes in your app and included them in your project URLs.

**Q: Static files are not loading**  
A: Ensure you have a `static/` directory and your settings are correct.

---

## More Help

- [GitHub Issues](https://github.com/ForceFledgling/cotlette/issues)
- [Cotlette Documentation](../.docs/index.md) 