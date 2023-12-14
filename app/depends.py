import json

from pydantic import ValidationError
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/sign-in/access-token", scheme_name="JWT")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
) -> UserOut:
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

    payload_str = str(payload["sub"]).replace("'", "\"")
    payload_dict = json.loads(payload_str)
    user = user_repo.get_user_by_username(db, payload_dict["username"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    is_superuser = False
    is_moderator = False
    if user.role_id == 1:
        is_superuser = True
    elif user.role_id == 3:
        is_moderator = True
    return UserOut(
        id=user.id,
        username=user.username,
        is_active=True,
        is_superuser=is_superuser,
        is_moderator=is_moderator,
    )
