# Raystack Development

## Running without installation

Raystack can be used without installing the library, just by cloning the repository.

### CLI Usage

To run management commands, use the `raystack.py` script in the project root:

```bash
# Create synchronous project
python3 raystack.py startproject myproject

# Create asynchronous project
python3 raystack.py startproject myproject --async

# Create project without home app
python3 raystack.py startproject myproject --no-home

# Create application
python3 raystack.py startapp myapp

# View available commands
python3 raystack.py help
```

### Using created projects

Created projects can also work without installing the library. Their `manage.py` will automatically find raystack in the `src` folder:

```bash
cd myproject
python3 manage.py help
python3 manage.py runserver
```

## Library installation

For production use, it's recommended to install the library:

```bash
pip install raystack
```

After installation, you can use standard commands:

```bash
raystack startproject myproject
raystack startapp myapp
```

## Project structure

```
raystack/
├── raystack.py          # CLI script for development
├── src/
│   └── raystack/        # Main library code
├── example/             # Synchronous project example
├── example_async/       # Asynchronous project example
└── test_projects/       # Test projects
```

## Compatibility

- CLI script `raystack.py` works only for development
- Created projects work both with installed library and without it
- `manage.py` templates automatically determine the raystack installation method

## Fixed issues

### Database import errors

When running commands, Python 3.6 warnings may appear, but this is not critical:

```
/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/jwt/utils.py:7: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography.
```

These warnings do not affect command operation and will disappear when using a newer Python version.

### Lazy imports

All database module imports are now performed lazily (lazy imports), which allows:
- Running commands without prior database configuration
- Avoiding circular dependencies
- Working both with installed library and without it
