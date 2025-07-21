from cotlette.shortcuts import render

# Create your views here.

# --- API ROUTES (moved from api.py) ---
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import timedelta, datetime
from .models import GroupModel
# from .utils import hash_password, generate_jwt, check_password

from starlette.responses import JSONResponse, \
    PlainTextResponse, \
    RedirectResponse, \
    StreamingResponse, \
    FileResponse, \
    HTMLResponse

from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

router = APIRouter()

# Создание таблицы при запуске приложения
@router.on_event("startup")
async def create_tables():
    GroupModel.create_table()
    owners_group = GroupModel.objects.filter(name="Owners").first()  # type: ignore
    if not owners_group:
        GroupModel.objects.create(name="Owners")

# (Закомментированные примеры моделей и ручек оставлены для истории)
