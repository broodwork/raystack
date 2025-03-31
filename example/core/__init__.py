from fastapi import FastAPI, Request

from cotlette import Cotlette


app = Cotlette()

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM

from cotlette.shortcuts import render_template




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




@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Проверяем, относится ли запрос к /admin/*
    if request.url.path.startswith("/admin"):
        token = request.cookies.get("access_token")  # Ищем токен в cookie
        if not token:
            # return JSONResponse(status_code=401, content={"detail": "Missing token"})
            return render_template(request=request, template_name="401.html", context={
                "url_for": url_for,
                # "parent": "/",
                # "segment": "test",
                "config": request.app.settings,
            })
        
        try:
            # Декодируем токен
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
    
    # Если токен валиден, продолжаем обработку запроса
    response = await call_next(request)
    return response