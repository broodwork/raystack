from fastapi import APIRouter, Request
from cotlette.shortcuts import render_template


router = APIRouter()


# Include your routes here.

# Example:
@router.get("/")
async def example(request: Request):    
    return render_template(request=request, template_name="home.html", context={})