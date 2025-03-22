import pathlib

# Базовая директория проекта
BASE_DIR = pathlib.Path(__file__).resolve().parent

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',  # Путь к файлу базы данных
    }
}