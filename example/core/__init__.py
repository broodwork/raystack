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


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool
    youmoney_client_id: str | None = None  # Добавьте эти поля, если они нужны
    youmoney_redirect_url: str | None = None
    youmoney_client_secret: str | None = None
    youmoney_access_token: str | None = None
    youmoney_wallet_number: str | None = None

    class Config:
        env_file = ".env"   # Указывает путь к .env файлу
        extra = 'ignore'    # Игнорировать лишние поля

# Инициализация объекта
settings = Settings(
    database_url="postgresql://user:password@localhost/dbname",
    secret_key="your-secret-key",
    debug=True
)


app = Cotlette()


from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse

@app.exception_handler(403)
async def not_found(request, exc):
    return RedirectResponse("/auth/accounts/login", status_code=303)
    # return render_template(request=request, template_name="401.html", context={"request": request})

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


# Middleware для работы с сессиями
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Middleware для аутентификации
app.add_middleware(AuthenticationMiddleware, backend=userAuthentication())


from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# # Функция, которая будет выполняться периодически
# def periodic_task():
#     print(f"Периодическая задача выполнена: {datetime.now()}")

# # Инициализация планировщика
# scheduler = BackgroundScheduler()

# # Добавление задачи для выполнения каждые 10 секунд
# scheduler.add_job(periodic_task, 'interval', seconds=10)

# # Запуск планировщика
# scheduler.start()