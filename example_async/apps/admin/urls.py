import os

from fastapi import APIRouter, Request

# from cotlette.conf import settings
from cotlette.shortcuts import render_template

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from config.settings import SECRET_KEY, ALGORITHM

from fastapi.security import OAuth2PasswordBearer

from starlette.authentication import requires

from apps.users.models import UserModel
from apps.groups.models import GroupModel


router = APIRouter()


def url_for(endpoint, **kwargs):
    """
    Функция для генерации URL на основе endpoint и дополнительных параметров.
    В данном случае endpoint игнорируется, так как мы используем только filename.
    """
    path = f"/{endpoint}"

    if not kwargs:
        return path
    
    for key, value in kwargs.items():
        path += f"/{value}"
    
    return path


@router.get("/users", response_model=None)
@requires("user_auth")
async def users_view(request: Request):
    users = await UserModel.objects.all().execute()  # type: ignore
    for user in users:
        print("user", user)

    return render_template(request=request, template_name="admin/users.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
        "users": users,
    })


@router.get("/groups", response_model=None)
@requires("user_auth")
async def groups_view(request: Request):
    groups = await GroupModel.objects.all().execute()  # type: ignore

    return render_template(request=request, template_name="admin/groups.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
        "groups": groups,
    })


@router.get("/", response_model=None)
@requires("user_auth")
async def index_view(request: Request):    
    return render_template(request=request, template_name="pages/index.html", context={
        "url_for": url_for,
        "parent": "home1",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/tables", response_model=None)
@requires("user_auth")
async def tables_view(request: Request):    
    return render_template(request=request, template_name="pages/tables.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/billing", response_model=None)
@requires("user_auth")
async def billing_view(request: Request):    
    return render_template(request=request, template_name="pages/billing.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/profile", response_model=None)
@requires("user_auth")
async def profile_view(request: Request):    
    return render_template(request=request, template_name="pages/profile.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })
