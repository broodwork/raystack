from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import AuthenticationBackend, SimpleUser, AuthCredentials
import jwt
from raystack.conf import settings

class JWTAuthentication(AuthenticationBackend):
    """JWT аутентификация для проверки токенов из cookies."""
    async def authenticate(self, request):
        jwt_token = request.cookies.get("jwt")
        if not jwt_token:
            return None
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return AuthCredentials(["user_auth", "admin"]), SimpleUser(str(user_id))
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.InvalidSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
            return None

class SimpleAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware для аутентификации с проверкой JWT токенов.
    """
    def __init__(self, app):
        super().__init__(app)
        self.auth_backend = JWTAuthentication()

    async def dispatch(self, request: Request, call_next):
        # Проверяем аутентификацию через JWT
        auth_result = await self.auth_backend.authenticate(request)
        
        if auth_result:
            credentials, user = auth_result
            request.scope["auth"] = credentials
            request.scope["user"] = user
        else:
            # Пользователь не аутентифицирован - создаем пустые объекты
            from starlette.authentication import AuthCredentials
            request.scope["auth"] = AuthCredentials([])  # Пустые права доступа
            request.scope["user"] = None
        
        response = await call_next(request)
        return response


class PermissionMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Check if this is an HTTP request
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Create Request object for convenience
        request = Request(scope, receive)

        # Для тестовых проектов пропускаем все запросы
        # В реальных проектах здесь должна быть настоящая проверка аутентификации
        await self.app(scope, receive, send)
        return
