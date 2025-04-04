from fastapi import FastAPI, Request
from cotlette import Cotlette
from fastapi.responses import JSONResponse, HTMLResponse
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from starlette.middleware.sessions import SessionMiddleware

from cotlette.shortcuts import render_template


app = Cotlette()


@app.exception_handler(403)
async def not_found(request, exc):
    context = {"request": request}
    # return templates.TemplateResponse("403.html", context, status_code=404)
    return render_template(request=request, template_name="401.html", context={})

# Класс для аутентификации
class userAuthentication(AuthenticationBackend):
    async def authenticate(self, request):
        jwt_cookie = request.cookies.get('jwt')
        if jwt_cookie:  # cookie exists
            try:
                payload = jwt.decode(jwt_cookie.encode('utf8'), str(SECRET_KEY), algorithms=[ALGORITHM])
                return AuthCredentials(["user_auth"]), SimpleUser(payload['user_id'])
            except:
                raise AuthenticationError('Invalid auth credentials')
        else:
            return  # unauthenticated

# Middleware для отслеживания истории
@app.middleware("http")
async def update_session_history(request, call_next):
    response = await call_next(request)
    history = request.session.setdefault('history', [])
    history.append(request.url.path)
    return response


# # Middleware для проверки прав доступа
# @app.middleware("http")
# async def verify_user(request, call_next):
#     print('request', request.__dict__)
#     if not hasattr(request, "user") or not request.user.is_authenticated:
#         return HTMLResponse('Forbidden', status_code=403)

#     if request.user.display_name == request.path_params.get('user_id'):
#         response = await call_next(request)
#         return response

#     return HTMLResponse('Forbidden', status_code=403)

# Middleware для работы с сессиями
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Middleware для аутентификации
app.add_middleware(AuthenticationMiddleware, backend=userAuthentication())