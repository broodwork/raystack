import pathlib

# Base project directory
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
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
    # 'cotlette.apps.admin',
    # 'cotlette.apps.users',
    'apps.home',
    'apps.admin',
    'apps.users',
    'apps.accounts',
    'apps.groups',
]

TEMPLATES = [
    {
        "BACKEND": "cotlette.template.backends.jinja2.Jinja2",
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