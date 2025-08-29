from fastapi import APIRouter, Request
from starlette.responses import JSONResponse, RedirectResponse
from raystack.contrib.auth.users.models import UserModel
from raystack.contrib.auth.users.utils import check_password, generate_jwt

router = APIRouter()

@router.post("/login")
async def login_user(request: Request):
    # Получаем данные формы
    form = await request.form()
    username = form.get("email")
    password = form.get("password")
    
    # Проверяем, что все поля заполнены
    if not username or not password:
        return RedirectResponse("/accounts/login?error=missing_fields", status_code=303)

    # Ищем пользователя
    user = await UserModel.objects.filter(email=username).first()  # type: ignore
    if not user:
        return RedirectResponse("/accounts/login?error=invalid_credentials", status_code=303)

    # Проверяем пароль
    hashed_pass = user.password_hash
    valid_pass = await check_password(password, hashed_pass)
    if not valid_pass:
        return RedirectResponse("/accounts/login?error=invalid_credentials", status_code=303)

    # Если все проверки пройдены, создаем JWT токен и перенаправляем в админку
    response = RedirectResponse("/admin/", status_code=303)
    response.set_cookie('jwt', generate_jwt(user.id), httponly=True, path="/")
    return response

@router.post("/logout")
async def logout(request: Request):
    # Создаем ответ с перенаправлением на страницу входа
    response = RedirectResponse(url="/accounts/login", status_code=303)
    
    # Очищаем JWT токен
    response.delete_cookie("jwt", path="/")
    
    # Также очищаем другие возможные токены
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    
    return response 