from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import timedelta
from .models import UserModel, UserCreate, User
from .utils import hash_password, generate_jwt, check_password

from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Pydantic-модель для входа пользователя
class UserLogin(BaseModel):
    email: str
    password: str

# Pydantic-модель для токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Pydantic-модель для данных токена
class TokenData(BaseModel):
    email: Union[str] = None


# TODO
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from jose import JWTError, jwt

# Настройки для JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Эндпоинт для аутентификации пользователя
# @router.post("/login/", response_model=Token)
# def login_for_access_token(user_login: UserLogin):
    
#     # Ищем пользователя по email
#     user = UserModel.objects.filter(email=user_login.email).first()

#     if not user or not check_password(user_login.password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = generate_jwt(
#         data={"user_id": user.id}, expires_delta=access_token_expires
#     )
#     # Создаем cookie с токеном
#     response = JSONResponse(content={"message": "Login successful"})
#     # response.set_cookie(
#     #     key="access_token",
#     #     value=access_token,
#     #     httponly=True,  # Защищает от доступа через JavaScript
#     #     # secure=True,    # Требует HTTPS (уберите для тестирования на localhost)
#     #     samesite="lax", # Защита от CSRF
#     #     max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
#     # )
#     response.set_cookie('jwt', generate_jwt(results['id']), httponly=True)

#     return response


@router.route("/login", methods=["POST"])
async def login_user(request):
    # Перенаправление на предыдущий путь после входа
    if 'history' in request.session and len(request.session['history']):
        previous = request.session['history'].pop()
    else:
        previous = '/'

    # Получение данных формы
    form = await request.form()
    username = form["email"]
    password = form["password"]

    # Поиск пользователя в базе данных
    user = UserModel.objects.filter(email=username).first()
    if not user:
        return RedirectResponse(previous, status_code=303)

    hashed_pass = user.password_hash

    # Проверка пароля
    valid_pass = await check_password(password, hashed_pass)
    if not valid_pass:
        return RedirectResponse(previous, status_code=303)

    if previous.count('/api/users/login'):
        previous = '/admin'

    response = RedirectResponse(previous, status_code=303)
    if valid_pass:
        response.set_cookie('jwt', generate_jwt(user.id), httponly=True)
    return response


@router.post("/logout", response_model=None)
def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("jwt")
    return response


# Создание таблицы при запуске приложения
@router.on_event("startup")
def create_tables():
    # print('UserModel', UserModel)
    UserModel.create_table()


from apps.groups.models import GroupModel

# Создание нового пользователя (POST)
@router.post("/", response_model=None)
async def create_user(user: UserCreate):
    hashed_password = await hash_password(user.password)
    group = GroupModel.objects.filter(id=user.group_id).first()

    new_user = UserModel.objects.create(
        name=user.name,
        age=user.age,
        email=user.email,
        password_hash=hashed_password,
        group=group.id
    )
    return User(
        name=new_user.name,
        age=new_user.age,
        email=new_user.email,
        group=new_user.group.id
    )


# Получение всех пользователей (GET)
@router.get("/", response_model=list[User])
def get_users():
    users = UserModel.objects.all()
    return [User(name=user.name, age=user.age, email=user.email) for user in users]