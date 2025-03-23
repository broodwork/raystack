from fastapi import APIRouter, Request
from cotlette.shortcuts import render

router = APIRouter()

import os



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


@router.get("/", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/index.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test"
    })

@router.get("/accounts_login", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="accounts/login.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test"
    })

@router.get("/tables", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/tables.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test"
    })



@router.get("/test", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/profile.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test"
    })
