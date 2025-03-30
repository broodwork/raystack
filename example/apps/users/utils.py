import bcrypt


def hash_password(password: str) -> str:
    # Хешируем пароль с использованием bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверяем, совпадает ли пароль
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))