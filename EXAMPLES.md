# Примеры использования шаблонов Cotlette

Этот документ содержит примеры создания и настройки проектов с использованием шаблонов Cotlette.

## Быстрый старт

### 1. Создание нового проекта

```bash
# Создать проект с приложением home
python manage.py startproject mywebsite

# Перейти в директорию проекта
cd mywebsite

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
alembic upgrade head

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
uvicorn core:app --reload
```

### 2. Структура созданного проекта

```
mywebsite/
├── apps/
│   └── home/               # Приложение home
│       ├── models.py       # Модель HomePage
│       ├── views.py        # Представления
│       ├── urls.py         # URL маршруты
│       ├── admin.py        # Админка
│       ├── api.py          # API
│       └── tests.py        # Тесты
├── config/
│   ├── settings.py         # Настройки
│   └── urls.py             # Главные URL
├── core/
│   └── __init__.py         # Инициализация
├── templates/
│   ├── base.html           # Базовый шаблон
│   └── home/               # Шаблоны home
├── requirements.txt         # Зависимости
└── README.md                # Документация
```

## Примеры настройки

### Настройка базы данных

#### SQLite (по умолчанию)

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
    }
}
```

#### PostgreSQL (асинхронно)

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'postgresql+asyncpg://user:password@localhost/dbname',
    }
}

# Установить драйвер
pip install asyncpg
```

#### MySQL (асинхронно)

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': 'mysql+aiomysql://user:password@localhost/dbname',
    }
}

# Установить драйвер
pip install aiomysql
```

### Настройка аутентификации

```python
# config/settings.py
SECRET_KEY = b'your-secret-key-here'
ALGORITHM = "HS256"

# Настройки JWT
JWT_SECRET_KEY = "your-jwt-secret"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Настройка статических файлов

```python
# config/settings.py
STATIC_URL = "static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

STATICFILES_DIRS = [
    str(BASE_DIR.parent / "cotlette" / "src" / "cotlette" / "contrib" / "static"),
    str(BASE_DIR / "static"),
]
```

## Примеры расширения

### Добавление нового поля в модель HomePage

```python
# apps/home/models.py
from cotlette.core.database import models

class HomePage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    # Новые поля
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Подзаголовок")
    featured_image = models.ImageField(upload_to='home/', blank=True, verbose_name="Изображение")
    meta_description = models.TextField(max_length=500, blank=True, verbose_name="Meta описание")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'home_page'
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главные страницы'
    
    def __str__(self):
        return self.title
```

### Создание нового представления

```python
# apps/home/views.py
from cotlette.shortcuts import render
from .models import HomePage

async def contact_view(request):
    """Страница контактов"""
    context = {
        'title': 'Контакты',
        'content': 'Свяжитесь с нами',
        'contact_info': {
            'email': 'info@example.com',
            'phone': '+7 (999) 123-45-67',
            'address': 'г. Москва, ул. Примерная, д. 1'
        }
    }
    return render(request, 'home/contact.html', context)

async def blog_view(request):
    """Страница блога"""
    try:
        posts = await HomePage.objects.filter(is_active=True).all()
        context = {
            'title': 'Блог',
            'posts': posts
        }
    except:
        context = {
            'title': 'Блог',
            'posts': []
        }
    
    return render(request, 'home/blog.html', context)
```

### Добавление новых URL

```python
# apps/home/urls.py
from fastapi import APIRouter, Request
from cotlette.shortcuts import render_template
from starlette.authentication import requires
from . import views

router = APIRouter()

# Существующие маршруты
@router.get("/")
async def home(request: Request):    
    return await views.home_view(request)

@router.get('/about')
async def about(request: Request):
    return await views.about_view(request)

@router.get('/private')
@requires('user_auth')
async def private_page(request: Request):
    context = {
        'title': 'Приватная страница',
        'message': 'Эта страница доступна только авторизованным пользователям!'
    }
    return render_template(request=request, template_name="home/private.html", context=context)

# Новые маршруты
@router.get('/contact')
async def contact(request: Request):
    return await views.contact_view(request)

@router.get('/blog')
async def blog(request: Request):
    return await views.blog_view(request)

@router.get('/blog/{post_id}')
async def blog_post(request: Request, post_id: int):
    try:
        post = await HomePage.objects.get(id=post_id)
        context = {
            'title': post.title,
            'post': post
        }
    except:
        context = {
            'title': 'Пост не найден',
            'post': None
        }
    
    return render_template(request=request, template_name="home/blog_post.html", context=context)
```

### Создание нового шаблона

```html
<!-- templates/home/contact.html -->
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row">
        <div class="col-12">
            <div class="card mb-4">
                <div class="card-header pb-0">
                    <h6>{{ title }}</h6>
                </div>
                <div class="card-body px-0 pt-0 pb-2">
                    <div class="p-4">
                        <div class="row">
                            <div class="col-md-6">
                                <h4>{{ title }}</h4>
                                <p class="text-muted">{{ content }}</p>
                                
                                <div class="mt-4">
                                    <h6>Контактная информация:</h6>
                                    <ul class="list-unstyled">
                                        <li><i class="fas fa-envelope text-primary me-2"></i>{{ contact_info.email }}</li>
                                        <li><i class="fas fa-phone text-primary me-2"></i>{{ contact_info.phone }}</li>
                                        <li><i class="fas fa-map-marker-alt text-primary me-2"></i>{{ contact_info.address }}</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <form>
                                    <div class="form-group">
                                        <label for="name">Имя</label>
                                        <input type="text" class="form-control" id="name" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="email">Email</label>
                                        <input type="email" class="form-control" id="email" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="message">Сообщение</label>
                                        <textarea class="form-control" id="message" rows="5" required></textarea>
                                    </div>
                                    <button type="submit" class="btn btn-primary mt-3">Отправить</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Расширение админки

```python
# apps/home/admin.py
from cotlette.contrib import admin
from .models import HomePage

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'subtitle', 'content', 'meta_description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
        ('Медиа', {
            'fields': ('featured_image',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Дополнительная логика при сохранении
        if not obj.meta_description:
            obj.meta_description = obj.content[:500] + "..." if len(obj.content) > 500 else obj.content
        super().save_model(request, obj, form, change)
```

### Создание API endpoints

```python
# apps/home/api.py
from fastapi import APIRouter, Request, HTTPException
from cotlette.shortcuts import render_template
from .models import HomePage
from typing import List

router = APIRouter()

@router.get("/api/home/data")
async def get_home_data(request: Request):
    """Получение данных главной страницы"""
    try:
        home_page = await HomePage.objects.filter(is_active=True).first()
        if home_page:
            return {
                "status": "success",
                "data": {
                    "title": home_page.title,
                    "subtitle": home_page.subtitle,
                    "content": home_page.content,
                    "meta_description": home_page.meta_description,
                    "featured_image": str(home_page.featured_image) if home_page.featured_image else None,
                    "created_at": home_page.created_at.isoformat() if home_page.created_at else None,
                    "updated_at": home_page.updated_at.isoformat() if home_page.updated_at else None
                }
            }
        else:
            return {
                "status": "success",
                "data": {
                    "title": "Добро пожаловать",
                    "subtitle": "",
                    "content": "Это главная страница вашего приложения.",
                    "meta_description": "",
                    "featured_image": None,
                    "created_at": None,
                    "updated_at": None
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/home/posts")
async def get_posts(request: Request, limit: int = 10, offset: int = 0):
    """Получение списка постов"""
    try:
        posts = await HomePage.objects.filter(is_active=True).limit(limit).offset(offset).all()
        return {
            "status": "success",
            "data": [
                {
                    "id": post.id,
                    "title": post.title,
                    "subtitle": post.subtitle,
                    "content": post.content[:200] + "..." if len(post.content) > 200 else post.content,
                    "created_at": post.created_at.isoformat() if post.created_at else None
                }
                for post in posts
            ],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": len(posts)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/home/update")
async def update_home_page(request: Request):
    """Обновление данных главной страницы"""
    try:
        # Здесь должна быть логика обновления
        # Для примера возвращаем успешный ответ
        return {
            "status": "success",
            "message": "Главная страница обновлена"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Тестирование

### Создание тестов

```python
# apps/home/tests.py
from cotlette.test import TestCase
from .models import HomePage

class HomeTestCase(TestCase):
    """Тесты для приложения home"""
    
    async def test_home_view(self):
        """Тест главной страницы"""
        response = await self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Добро пожаловать')
    
    async def test_about_view(self):
        """Тест страницы 'О нас'"""
        response = await self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'О нас')
    
    async def test_contact_view(self):
        """Тест страницы контактов"""
        response = await self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Контакты')
    
    async def test_private_page_requires_auth(self):
        """Тест что приватная страница требует авторизации"""
        response = await self.client.get('/private')
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    async def test_home_api_data(self):
        """Тест API для получения данных главной страницы"""
        response = await self.client.get('/api/home/data')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
    
    async def test_home_api_posts(self):
        """Тест API для получения постов"""
        response = await self.client.get('/api/home/posts?limit=5')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        self.assertIn('pagination', data)


class HomeModelTestCase(TestCase):
    """Тесты для моделей приложения home"""
    
    async def test_home_page_creation(self):
        """Тест создания модели HomePage"""
        home_page = await HomePage.objects.create(
            title='Тестовая страница',
            subtitle='Тестовый подзаголовок',
            content='Тестовое содержание',
            meta_description='Тестовое meta описание'
        )
        self.assertEqual(home_page.title, 'Тестовая страница')
        self.assertEqual(home_page.subtitle, 'Тестовый подзаголовок')
        self.assertEqual(home_page.content, 'Тестовое содержание')
        self.assertEqual(home_page.meta_description, 'Тестовое meta описание')
        self.assertTrue(home_page.is_active)
    
    async def test_home_page_str_representation(self):
        """Тест строкового представления модели"""
        home_page = await HomePage.objects.create(
            title='Тестовая страница',
            content='Тестовое содержание'
        )
        self.assertEqual(str(home_page), 'Тестовая страница')
    
    async def test_home_page_defaults(self):
        """Тест значений по умолчанию"""
        home_page = await HomePage.objects.create(
            title='Тестовая страница',
            content='Тестовое содержание'
        )
        self.assertTrue(home_page.is_active)
        self.assertIsNotNone(home_page.created_at)
        self.assertIsNotNone(home_page.updated_at)
```

### Запуск тестов

```bash
# Запустить все тесты
python manage.py test

# Запустить тесты конкретного приложения
python manage.py test apps.home

# Запустить конкретный тест
python manage.py test apps.home.tests.HomeTestCase.test_home_view

# Запустить тесты с подробным выводом
python manage.py test -v 2
```

## Развертывание

### Настройка для продакшна

```python
# config/settings.py
import os

# Базовые настройки
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Настройки безопасности
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() == 'true'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'cotlette.core.database.sqlalchemy',
        'URL': os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
    }
}

# Настройки статических файлов
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))
STATIC_URL = os.getenv('STATIC_URL', '/static/')

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директории для логов
RUN mkdir -p logs

# Применение миграций
RUN alembic upgrade head

# Сбор статических файлов
RUN python manage.py collectstatic --noinput

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "core:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=dbname
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Заключение

Эти примеры демонстрируют, как использовать шаблоны Cotlette для быстрого создания полнофункциональных веб-приложений. Шаблоны предоставляют:

- Готовую структуру проекта
- Базовую функциональность
- Современный UI
- API готовность
- Систему аутентификации
- Админ-панель
- Тесты

Используйте эти примеры как отправную точку для создания собственных проектов на базе Cotlette.

