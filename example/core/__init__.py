from fastapi import FastAPI, Request

from cotlette import Cotlette


app = Cotlette()

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Проверяем, относится ли запрос к /admin/*
    if request.url.path.startswith("/admin"):
        token = request.cookies.get("access_token")  # Ищем токен в cookie
        if not token:
            return JSONResponse(status_code=401, content={"detail": "Missing token"})
        
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