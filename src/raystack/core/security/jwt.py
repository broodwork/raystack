from typing import Optional, Union, Any
import jwt
from datetime import datetime, timedelta

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # Default 30 minutes
    
    # Get settings safely
    try:
        from raystack.conf import settings
        secret_key = getattr(settings, 'SECRET_KEY', 'default-secret-key')
        algorithm = getattr(settings, 'ALGORITHM', 'HS256')
    except ImportError:
        secret_key = 'default-secret-key'
        algorithm = 'HS256'
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt