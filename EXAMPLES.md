# Raystack Templates Usage Examples

This document provides examples for creating and configuring projects using Raystack templates.

## Quick Start

### 1. Create a New Project

```bash
# Create a project with a home app
raystack startproject mywebsite

# Navigate to the project directory
cd mywebsite

# Install dependencies
pip install -r requirements.txt

# Apply migrations
alembic upgrade head

# Create a superuser
raystack createsuperuser

# Run the server
raystack runserver
```

### 2. Structure of the Created Project

```
mywebsite/
├── apps/
│   └── home/               # Home application
│       ├── models.py       # HomePage model
│       ├── views.py        # Views
│       ├── urls.py         # URL routes
│       ├── admin.py        # Admin configuration
│       ├── api.py          # API endpoints
│       └── tests.py        # Tests
├── config/
│   ├── settings.py         # Settings
│   └── urls.py             # Main URLs
├── core/
│   └── __init__.py         # Initialization
├── templates/
│   ├── base.html           # Base template
│   └── home/               # Home templates
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## Configuration Examples

### Database Configuration

#### SQLite (Default)

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'raystack.core.database.sqlalchemy',
        'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
    }
}
```

#### PostgreSQL (Asynchronous)

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'raystack.core.database.sqlalchemy',
        'URL': 'postgresql+asyncpg://user:password@localhost/dbname',
    }
}

# Install driver
pip install asyncpg
```

#### MySQL (Asynchronous)

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'raystack.core.database.sqlalchemy',
        'URL': 'mysql+aiomysql://user:password@localhost/dbname',
    }
}

# Install driver
pip install aiomysql
```

### Authentication Configuration

```python
# config/settings.py
SECRET_KEY = b'your-secret-key-here'
ALGORITHM = "HS256"

# JWT Settings
JWT_SECRET_KEY = "your-jwt-secret"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Static Files Configuration

```python
# config/settings.py
STATIC_URL = "static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

STATICFILES_DIRS = [
    str(BASE_DIR.parent / "raystack" / "src" / "raystack" / "contrib" / "static"),
    str(BASE_DIR / "static"),
]
```

## Extension Examples

### Adding a New Field to the HomePage Model

```python
# apps/home/models.py
from raystack.core.database import models

class HomePage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    # New fields
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Subtitle")
    featured_image = models.ImageField(upload_to='home/', blank=True, verbose_name="Featured Image")
    meta_description = models.TextField(max_length=500, blank=True, verbose_name="Meta Description")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    
    class Meta:
        db_table = 'home_page'
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'
    
    def __str__(self):
        return self.title
```

### Creating a New View

```python
# apps/home/views.py
from raystack.shortcuts import render
from .models import HomePage

async def contact_view(request):
    """Contact Page"""
    context = {
        'title': 'Contact Us',
        'content': 'Get in touch with us',
        'contact_info': {
            'email': 'info@example.com',
            'phone': '+7 (999) 123-45-67',
            'address': 'Moscow, Example St., 1'
        }
    }
    return render(request, 'home/contact.html', context)

async def blog_view(request):
    """Blog Page"""
    try:
        posts = await HomePage.objects.filter(is_active=True).all()
        context = {
            'title': 'Blog',
            'posts': posts
        }
    except:
        context = {
            'title': 'Blog',
            'posts': []
        }
    
    return render(request, 'home/blog.html', context)
```

### Adding New URLs

```python
# apps/home/urls.py
from fastapi import APIRouter, Request
from raystack.shortcuts import render_template
from starlette.authentication import requires
from . import views

router = APIRouter()

# Existing routes
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
        'title': 'Private Page',
        'message': 'This page is only accessible to authenticated users!'
    }
    return render_template(request=request, template_name="home/private.html", context=context)

# New routes
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
            'title': 'Post not found',
            'post': None
        }
    
    return render_template(request=request, template_name="home/blog_post.html", context=context)
```

### Creating a New Template

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
                                    <h6>Contact Information:</h6>
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
                                        <label for="name">Name</label>
                                        <input type="text" class="form-control" id="name" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="email">Email</label>
                                        <input type="email" class="form-control" id="email" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="message">Message</label>
                                        <textarea class="form-control" id="message" rows="5" required></textarea>
                                    </div>
                                    <button type="submit" class="btn btn-primary mt-3">Send</button>
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

### Extending the Admin Panel

```python
# apps/home/admin.py
from raystack.contrib import admin
from .models import HomePage

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'subtitle', 'content', 'meta_description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Main Information', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('SEO', {
            'fields': ('meta_description',)
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Additional logic on save
        if not obj.meta_description:
            obj.meta_description = obj.content[:500] + "..." if len(obj.content) > 500 else obj.content
        super().save_model(request, obj, form, change)
```

### Creating API Endpoints

```python
# apps/home/api.py
from fastapi import APIRouter, Request, HTTPException
from raystack.shortcuts import render_template
from .models import HomePage
from typing import List

router = APIRouter()

@router.get("/api/home/data")
async def get_home_data(request: Request):
    """Get home page data"""
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
                    "title": "Welcome",
                    "subtitle": "",
                    "content": "This is the home page of your application.",
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
    """Get a list of posts"""
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
    """Update home page data"""
    try:
        # Update logic here
        # For example, return a successful response
        return {
            "status": "success",
            "message": "Home page updated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Testing

### Creating Tests

```python
# apps/home/tests.py
from raystack.test import TestCase
from .models import HomePage

class HomeTestCase(TestCase):
    """Tests for the home app"""
    
    async def test_home_view(self):
        """Test the home page"""
        response = await self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')
    
    async def test_about_view(self):
        """Test the 'About Us' page"""
        response = await self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')
    
    async def test_contact_view(self):
        """Test the contact page"""
        response = await self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')
    
    async def test_private_page_requires_auth(self):
        """Test that the private page requires authentication"""
        response = await self.client.get('/private')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    async def test_home_api_data(self):
        """Test API for getting home page data"""
        response = await self.client.get('/api/home/data')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
    
    async def test_home_api_posts(self):
        """Test API for getting posts"""
        response = await self.client.get('/api/home/posts?limit=5')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('data', data)
        self.assertIn('pagination', data)


class HomeModelTestCase(TestCase):
    """Tests for models of the home app"""
    
    async def test_home_page_creation(self):
        """Test HomePage model creation"""
        home_page = await HomePage.objects.create(
            title='Test Page',
            subtitle='Test Subtitle',
            content='Test Content',
            meta_description='Test meta description'
        )
        self.assertEqual(home_page.title, 'Test Page')
        self.assertEqual(home_page.subtitle, 'Test Subtitle')
        self.assertEqual(home_page.content, 'Test Content')
        self.assertEqual(home_page.meta_description, 'Test meta description')
        self.assertTrue(home_page.is_active)
    
    async def test_home_page_str_representation(self):
        """Test string representation of the model"""
        home_page = await HomePage.objects.create(
            title='Test Page',
            content='Test Content'
        )
        self.assertEqual(str(home_page), 'Test Page')
    
    async def test_home_page_defaults(self):
        """Test default values"""
        home_page = await HomePage.objects.create(
            title='Test Page',
            content='Test Content'
        )
        self.assertTrue(home_page.is_active)
        self.assertIsNotNone(home_page.created_at)
        self.assertIsNotNone(home_page.updated_at)
```

### Running Tests

```bash
# Run all tests
raystack test

# Run tests for a specific app
raystack test apps.home

# Run a specific test
raystack test apps.home.tests.HomeTestCase.test_home_view

# Run tests with verbose output
raystack test -v 2
```

## Deployment

### Production Configuration

```python
# config/settings.py
import os

# Base settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() == 'true'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'raystack.core.database.sqlalchemy',
        'URL': os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
    }
}

# Static files settings
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))
STATIC_URL = os.getenv('STATIC_URL', '/static/')

# Logging
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

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Apply migrations
RUN alembic upgrade head

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
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

## Conclusion

These examples demonstrate how to use Raystack templates to quickly create full-featured web applications. The templates provide:

- A ready-to-use project structure
- Basic functionality
- Modern UI
- API readiness
- Authentication system
- Admin panel
- Tests

Use these examples as a starting point for building your own Raystack projects.
