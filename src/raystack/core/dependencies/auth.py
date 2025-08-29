from collections.abc import Generator
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from raystack.core.database.base import get_async_db, async_engine # Используем асинхронный движок
from raystack.core.security.jwt import create_access_token # Чтобы не было циклической зависимости

# Safe import to avoid circular dependency
try:
    from raystack.conf import settings
    API_V1_STR = getattr(settings, 'API_V1_STR', '/api/v1')
    SECRET_KEY = getattr(settings, 'SECRET_KEY', 'default-secret-key')
    ALGORITHM = getattr(settings, 'ALGORITHM', 'HS256')
except ImportError:
    API_V1_STR = '/api/v1'
    SECRET_KEY = 'default-secret-key'
    ALGORITHM = 'HS256'

# TODO: Define a base User model in raystack.contrib.auth.models that these projects can import
# For now, we'll assume a User model exists in the project's models.py for demonstration.
# from your_project.models import TokenPayload, User 
# (This is a placeholder and will need to be addressed later.)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{API_V1_STR}/login/access-token"
)

def get_db():
    with Session(async_engine) as session: # Используем async_engine для создания синхронной сессии
        yield session

# For Python 3.6 compatibility, we'll use regular types instead of Annotated
SessionDep = Session
TokenDep = str

# Placeholder for User and TokenPayload models. These need to be imported from the actual project.
# We will assume that `example_async.models.User` and `example_async.models.TokenPayload` are available for now.
# In a real scenario, Raystack might provide a base User model or a way to register project-specific models.

# Mock models for now to avoid immediate import errors. These should be replaced by actual models.
class TokenPayload:
    sub: str

class User:
    id: int
    is_active: bool
    is_superuser: bool

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        # TODO: Replace with actual TokenPayload model from the project
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload) # Needs to be project specific
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # TODO: Replace with actual User model from the project
    user = session.get(User, token_data.sub) # Needs to be project specific
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = User

def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user