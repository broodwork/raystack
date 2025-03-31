import os

from fastapi import APIRouter, Request

# from cotlette.conf import settings
from cotlette.shortcuts import render_template

router = APIRouter()


def url_for(endpoint, **kwargs):
    """
    Функция для генерации URL на основе endpoint и дополнительных параметров.
    В данном случае endpoint игнорируется, так как мы используем только filename.
    """
    if not kwargs:
        return f"/{endpoint}"
    
    path = f"/{endpoint}"
    for key, value in kwargs.items():
        path += f"/{value}"
    
    return path


from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from config.settings import SECRET_KEY, ALGORITHM

from fastapi.security import OAuth2PasswordBearer


@router.get("/login", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="accounts/login.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": request.app.settings,
    })

@router.post("/logout", response_model=None)
def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response

@router.get("/register", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="accounts/register.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/password_change", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="accounts/password_change.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })