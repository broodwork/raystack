# Raystack Project Templates

This document describes how to use templates to create new projects and applications within the Raystack framework.

## Creating a New Project

### Basic Project with Home App

```bash
python manage.py startproject myproject
```

This command will create a new project with the following structure:

```
myproject/
├── apps/
│   └── home/               # Home application with basic functionality
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py       # HomePage model
│       ├── views.py        # Views for the main page
│       ├── urls.py         # URL routes
│       ├── admin.py        # Admin for HomePage
│       ├── api.py          # API endpoints
│       ├── controlles.py   # Controllers
│       └── tests.py        # Tests
├── config/
│   ├── settings.py         # Settings with async DB support
│   └── urls.py             # Main URLs with home app included
├── core/
│   └── __init__.py         # Initialization with middleware
├── templates/
│   ├── base.html           # Base template with navigation
│   └── home/               # Home app templates
│       ├── home.html       # Main page
│       ├── about.html      # About Us page
│       └── private.html    # Private page
├── static/                  # Static files
├── migrations/              # Alembic migrations
├── requirements.txt         # Dependencies
├── alembic.ini             # Alembic configuration
└── README.md                # Project documentation
```

### Project without Home App

```bash
python manage.py startproject myproject --no-home
```

### Project with Explicit Home App

```bash
python manage.py startproject myproject --with-home
```

## Creating a New Application

### Regular Application

```bash
python manage.py startapp myapp
```

### Home Application with Extended Functionality

```bash
python manage.py startapp_home myapp
```

This command will create an application with all necessary components:

- **Models** - basic model structure
- **Views** - example views
- **URL routes** - basic routes
- **Admin** - admin panel configuration
- **API** - REST API endpoints
- **Controllers** - controller classes
- **Tests** - basic tests
- **Templates** - HTML templates (if enabled)

### Options for startapp_home

```bash
# Create app without templates
python manage.py startapp_home myapp --no-templates

# Create app without admin
python manage.py startapp_home myapp --no-admin

# Create app without API
python manage.py startapp_home myapp --no-api
```

## Template Features

### Asynchronous Database Support

Templates support both synchronous and asynchronous databases:

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'raystack.core.database.sqlalchemy',
        # Synchronous mode
        'URL': 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        
        # Asynchronous mode
        # 'URL': 'sqlite+aiosqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        # 'URL': 'postgresql+asyncpg://user:pass@localhost/dbname',
        # 'URL': 'mysql+aiomysql://user:pass@localhost/dbname',
    }
}
```

### Built-in Authentication

Projects include:

- JWT authentication
- Session middleware
- Protected pages
- Role and permission system

### Modern UI

- Bootstrap 5
- Soft UI Dashboard
- Responsive design
- Font Awesome icons
- Dark/light theme

### API Readiness

- REST API endpoints
- Swagger/OpenAPI documentation
- Token authentication
- Error handling

## Setup After Creation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Edit `config/settings.py` and specify connection parameters.

### 3. Apply Migrations

```bash
alembic upgrade head
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Server

```bash
uvicorn core:app --reload
```

## Template Customization

### Adding New Fields to Models

```python
# apps/home/models.py
class HomePage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Add new fields here
    image = models.ImageField(upload_to='home/', blank=True)
    published_date = models.DateField(auto_now_add=True)
```

### Creating New Views

```python
# apps/home/views.py
async def contact_view(request):
    context = {
        'title': 'Contact Us',
        'content': 'Get in touch with us'
    }
    return render(request, 'home/contact.html', context)
```

### Adding New URLs

```python
# apps/home/urls.py
@router.get('/contact')
async def contact(request: Request):
    return await views.contact_view(request)
```

## Template Structure

### Application Templates

```
templates/
└── home/
    ├── home.html      # Main page
    ├── about.html     # About Us page
    └── private.html   # Private page
```

### Base Template

`base.html` includes:

- Navigation menu
- Sidebar
- Breadcrumbs
- Search
- Footer
- CSS/JS integration

## Testing

### Running Tests

```bash
python manage.py test
```

### Default Tests

- View tests
- Model tests
- API tests
- Authentication tests

## Deployment

### Production Settings

```python
# config/settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Static Files

```bash
python manage.py collectstatic
```

## Support

For support:

1. Refer to Raystack documentation
2. Check examples in `example/` and `example_async/`
3. Create an issue in the repository
4. Contact the developer community

## License

Templates are distributed under the same license as the Raystack framework.

