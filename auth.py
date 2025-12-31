from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def create_token(email: str):
    return jwt.encode(
        {
            "sub": email,
            "exp": datetime.utcnow() + timedelta(hours=12)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
