import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.config import env
from app.database import db_manager
from app.utils import decode_token, validate_date_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/sign-in/access-token", scheme_name="JWT"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = decode_token(token, env.JWT_SECRET_KEY)
        if not validate_date_token(payload):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload_str = str(payload["sub"]).replace("'", '"')
    payload_dict = json.loads(payload_str)
    try:
        user = db_manager.execute_query(
            'SELECT * FROM "User" WHERE email=%s', (payload_dict["email"],)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error accessing the database",
        ) from e
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return {"id": user.id, "username": user.username}
