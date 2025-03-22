import pathlib

# Базовая директория проекта
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

print('BASE_DIR', BASE_DIR)

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',  # Путь к файлу базы данных
    }
}

ALLOWED_HOSTS = ['*']

DEBUG = False

INSTALLED_APPS = []