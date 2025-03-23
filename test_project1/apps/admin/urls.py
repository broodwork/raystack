from fastapi import APIRouter, Request
from cotlette.shortcuts import render

router = APIRouter()

@router.get("/test", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="blank.html", context={"config": {
        "ASSETS_ROOT": "static/assets",
        "APP_NAME": "Cotlette"
    }})