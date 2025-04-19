import pathlib

# Базовая директория проекта
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
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