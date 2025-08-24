# Шаблоны проектов Cotlette

Этот документ описывает, как использовать шаблоны для создания новых проектов и приложений в фреймворке Cotlette.

## Создание нового проекта

### Базовый проект с приложением home

```bash
python manage.py startproject myproject
```

Эта команда создаст новый проект со следующей структурой:

```
myproject/
├── apps/
│   └── home/               # Приложение home с базовой функциональностью
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py       # Модель HomePage
│       ├── views.py        # Представления для главной страницы
│       ├── urls.py         # URL маршруты
│       ├── admin.py        # Админка для HomePage
│       ├── api.py          # API endpoints
│       ├── controlles.py   # Контроллеры
│       └── tests.py        # Тесты
├── config/
│   ├── settings.py         # Настройки с поддержкой асинхронных БД
│   └── urls.py             # Главные URL с подключением home
├── core/
│   └── __init__.py         # Инициализация с middleware
├── templates/
│   ├── base.html           # Базовый шаблон с навигацией
│   └── home/               # Шаблоны приложения home
│       ├── home.html       # Главная страница
│       ├── about.html      # Страница "О нас"
│       └── private.html    # Приватная страница
├── static/                  # Статические файлы
├── migrations/              # Миграции Alembic
├── requirements.txt         # Зависимости
├── alembic.ini             # Конфигурация Alembic
└── README.md                # Документация проекта
```

### Проект без приложения home

```bash
python manage.py startproject myproject --no-home
```

### Проект с явным указанием приложения home

```bash
python manage.py startproject myproject --with-home
```

## Создание нового приложения

### Обычное приложение

```bash
python manage.py startapp myapp
```

### Приложение home с расширенной функциональностью

```bash
python manage.py startapp_home myapp
```

Эта команда создаст приложение со всеми необходимыми компонентами:

- **Модели** - базовая структура для моделей
- **Представления** - примеры представлений
- **URL маршруты** - базовые маршруты
- **Админка** - конфигурация для админ-панели
- **API** - REST API endpoints
- **Контроллеры** - классы контроллеров
- **Тесты** - базовые тесты
- **Шаблоны** - HTML шаблоны (если включены)

### Опции для startapp_home

```bash
# Создать приложение без шаблонов
python manage.py startapp_home myapp --no-templates

# Создать приложение без админки
python manage.py startapp_home myapp --no-admin

# Создать приложение без API
python manage.py startapp_home myapp --no-api
```

## Особенности шаблонов

### Поддержка асинхронных баз данных

Шаблоны поддерживают как синхронные, так и асинхронные базы данных:

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        # Синхронный режим
        'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        
        # Асинхронный режим
        # 'URL': 'sqlite+aiosqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        # 'URL': 'postgresql+asyncpg://user:pass@localhost/dbname',
        # 'URL': 'mysql+aiomysql://user:pass@localhost/dbname',
    }
}
```

### Встроенная аутентификация

Проекты включают:

- JWT аутентификацию
- Middleware для сессий
- Защищенные страницы
- Система ролей и разрешений

### Современный UI

- Bootstrap 5
- Soft UI Dashboard
- Адаптивный дизайн
- Font Awesome иконки
- Темная/светлая тема

### API готовность

- REST API endpoints
- Swagger/OpenAPI документация
- Аутентификация через токены
- Обработка ошибок

## Настройка после создания

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных

Отредактируйте `config/settings.py` и укажите параметры подключения.

### 3. Применение миграций

```bash
alembic upgrade head
```

### 4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

```bash
uvicorn core:app --reload
```

## Кастомизация шаблонов

### Добавление новых полей в модели

```python
# apps/home/models.py
class HomePage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Добавьте новые поля здесь
    image = models.ImageField(upload_to='home/', blank=True)
    published_date = models.DateField(auto_now_add=True)
```

### Создание новых представлений

```python
# apps/home/views.py
async def contact_view(request):
    context = {
        'title': 'Контакты',
        'content': 'Свяжитесь с нами'
    }
    return render(request, 'home/contact.html', context)
```

### Добавление новых URL

```python
# apps/home/urls.py
@router.get('/contact')
async def contact(request: Request):
    return await views.contact_view(request)
```

## Структура шаблонов

### Шаблоны приложений

```
templates/
└── home/
    ├── home.html      # Главная страница
    ├── about.html     # Страница "О нас"
    └── private.html   # Приватная страница
```

### Базовый шаблон

`base.html` включает:

- Навигационное меню
- Боковая панель
- Хлебные крошки
- Поиск
- Футер
- Подключение CSS/JS

## Тестирование

### Запуск тестов

```bash
python manage.py test
```

### Тесты по умолчанию

- Тесты представлений
- Тесты моделей
- Тесты API
- Тесты аутентификации

## Развертывание

### Продакшн настройки

```python
# config/settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Настройки безопасности
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Статические файлы

```bash
python manage.py collectstatic
```

## Поддержка

Для получения поддержки:

1. Ознакомьтесь с документацией Cotlette
2. Проверьте примеры в `example/` и `example_async/`
3. Создайте issue в репозитории
4. Обратитесь к сообществу разработчиков

## Лицензия

Шаблоны распространяются под той же лицензией, что и фреймворк Cotlette.
