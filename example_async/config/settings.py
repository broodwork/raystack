import pathlib

# Base project directory
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'raystack.core.database.sqlalchemy',
        # Синхронный режим (по умолчанию)
        # 'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        
        # Асинхронный режим (раскомментируйте для использования)
        'URL': 'sqlite+aiosqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        
        # Другие примеры асинхронных URL:
        # PostgreSQL: 'postgresql+asyncpg://user:pass@localhost/dbname'
        # MySQL: 'mysql+aiomysql://user:pass@localhost/dbname'
    }
}

ALLOWED_HOSTS = ['*']

DEBUG = True

INSTALLED_APPS = [
    # 'raystack.apps.admin',
    # 'raystack.apps.users',
    'apps.home',
    'raystack.contrib.admin',
    'raystack.contrib.auth.users',
    'raystack.contrib.auth.accounts',
    'raystack.contrib.auth.groups',
]

TEMPLATES = [
    {
        "BACKEND": "raystack.template.backends.jinja2.Jinja2",
        "DIRS": [
            "templates",
            "jinja2"
        ],
        "APP_DIRS": True
    },
]

SECRET_KEY = b'$2b$12$SE0dQGdt3D260TqXQzuzbOcN2EqVqzFbn4nlNvfsgburDCYp2UvAS'
ALGORITHM = "HS256"

STATIC_URL = "static/"

# Настройки статических файлов
STATICFILES_DIRS = [
    str(BASE_DIR.parent / "raystack" / "src" / "raystack" / "contrib" / "static"),
    str(BASE_DIR / "static"),
]

STATIC_ROOT = str(BASE_DIR / "staticfiles")