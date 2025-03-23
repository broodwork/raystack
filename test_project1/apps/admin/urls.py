from fastapi import APIRouter, Request
from cotlette.shortcuts import render

router = APIRouter()

import os



def url_for(endpoint, **kwargs):
    """
    Функция для генерации URL на основе endpoint и дополнительных параметров.
    В данном случае endpoint игнорируется, так как мы используем только filename.
    """
    if endpoint == "static":
        filename = kwargs.get("filename")
        if filename:
            return f"static/{filename}"
    return ""



@router.get("/test", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/billing.html", context={
        "config": {
            "ASSETS_ROOT": "static/assets",
            "APP_NAME": "Cotlette"
        },
        "url_for": url_for,
        "parent": "/",
        "segment": "test"
    })
