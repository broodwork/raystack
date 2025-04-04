from fastapi import APIRouter, Request
from cotlette.shortcuts import render_template


router = APIRouter()


# Include your routes here.

# Example:
@router.get("/")
async def example(request: Request):    
    return render_template(request=request, template_name="home.html", context={})


from starlette.authentication import requires
@router.get('/private')
@requires('user_auth')  # protected endpoint, any authorized user can access it
async def users(request: Request):
    return render_template(request=request, template_name="home.html", context={})

@router.route('/test')
async def user(request):
    user_id = request.path_params['user_id']
    content = {
        "name": "GOOD",
    }
    return JSONResponse(content)