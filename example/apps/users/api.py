from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .models import UserModel, UserCreate, User
from .utils import hash_password

# Конфигурация JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
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

# Функция для создания JWT-токена
def create_access_token(data: dict, expires_delta: Union[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Эндпоинт для аутентификации пользователя
@router.post("/login/", response_model=Token)
def login_for_access_token(user_login: UserLogin):
    # Ищем пользователя по email
    user = UserModel.objects.filter(email=user_login.email).first()
    if not user or not UserModel.verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Создание таблицы при запуске приложения
@router.on_event("startup")
def create_tables():
    UserModel.create_table()


# Создание нового пользователя (POST)
@router.post("/users/", response_model=None)
def create_user(user: UserCreate):
    hashed_password = hash_password(user.password)
    new_user = UserModel.objects.create(
        name=user.name,
        age=user.age,
        email=user.email,
        password_hash=hashed_password
    )
    return User(
        name=new_user.name,
        age=new_user.age,
        email=new_user.email
    )


# Получение всех пользователей (GET)
@router.get("/users/", response_model=list[User])
def get_users():
    users = UserModel.objects.all()
    return [User(name=user.name, age=user.age, email=user.email) for user in users]