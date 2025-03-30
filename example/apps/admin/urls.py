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


# @router.get("/", response_model=None)
# async def test(request: Request):    
#     return render_template(request=request, template_name="pages/index.html", context={
#         "url_for": url_for,
#         "parent": "home1",
#         "segment": "test",
#         "config": request.app.settings,
#     })


# TODO



from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from config.settings import SECRET_KEY
ALGORITHM = "HS256"

from fastapi.security import OAuth2PasswordBearer
# Создаем схему для извлечения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Проверяет токен и извлекает email пользователя.
    """
    print('token', token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return email

# @router.get("/", response_model=None)
# async def test(
#     request: Request,
#     current_user: str = Depends(get_current_user)  # Проверяем токен
# ):
#     """
#     Защищенный эндпоинт, доступный только авторизованным пользователям.
#     """
#     print('request', request)
#     return render_template(
#         request=request,
#         # template_name="pages/index.html",
#         template_name="pages/protected.html",
#         context={
#             "url_for": url_for,
#             "parent": "home1",
#             "segment": "test",
#             "config": request.app.settings,
#             "user_email": current_user,  # Передаем email пользователя в контекст
#         },
#     )

@router.get("/", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="pages/protected.html", context={
        "url_for": url_for,
        "parent": "home1",
        "segment": "test",
        "config": request.app.settings,
    })


# Защищенный эндпоинт
@router.get("/protected")
async def protected_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}






@router.get("/accounts_login", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="accounts/login.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/accounts_register", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="accounts/register.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/pages_tables", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="pages/tables.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })



@router.get("/pages_billing", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="pages/billing.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/pages_profile", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="pages/profile.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })

@router.get("/accounts_password_change", response_model=None)
async def test(request: Request):    
    return render_template(request=request, template_name="accounts/password_change.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": request.app.settings,
    })