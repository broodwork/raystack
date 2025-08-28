# Raystack Middleware

## Overview

Middleware in Raystack allows you to process requests and responses globally, similar to Django or FastAPI middleware. You can use built-in middleware or write your own for cross-cutting concerns like authentication, logging, or CORS.

---

## Built-in Middleware

Raystack includes (or plans to include):
- Authentication middleware
- Session middleware
- CSRF protection (planned)
- Static files middleware

---

## Writing Custom Middleware

A middleware is a callable that takes a request and a handler, and returns a response. You can register middleware in your project settings or app configuration.

Example:
```python
from raystack.core.middlewares import BaseMiddleware

class CustomHeaderMiddleware(BaseMiddleware):
    async def __call__(self, request, call_next):
        response = await call_next(request)
        response.headers['X-Custom-Header'] = 'Raystack'
        return response
```

Register middleware in your app or project:
```python
app.add_middleware(CustomHeaderMiddleware)
```

---

## Middleware Order

Middleware are executed in the order they are added. The order matters for things like authentication and session management.

---

## Use Cases

- Authentication and authorization
- Logging and monitoring
- CORS
- GZip compression
- Request/response transformation

---

## Best Practices

- Keep middleware stateless if possible
- Use middleware for cross-cutting concerns
- Avoid heavy computation in middleware

---

## More

See [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) for advanced patterns (Raystack is compatible with FastAPI middleware API). 