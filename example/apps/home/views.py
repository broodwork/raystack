from raystack.shortcuts import render_template
from fastapi import Request

# Create your views here.

async def home_view(request: Request):
    return render_template(request, "home/home.html", context={"framework": "Raystack"})
