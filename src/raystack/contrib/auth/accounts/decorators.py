from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.authentication import has_required_scope


def login_required(required_scopes=None):
    """
    Декоратор для проверки аутентификации.
    Если пользователь не аутентифицирован, перенаправляет на страницу входа.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Проверяем, есть ли у пользователя необходимые права
            if not has_required_scope(request, required_scopes or []):
                # Перенаправляем на страницу входа
                return RedirectResponse(url="/accounts/login", status_code=303)
            
            # Если все проверки пройдены, вызываем оригинальную функцию
            return await func(request, *args, **kwargs)
        
        return wrapper
    return decorator

