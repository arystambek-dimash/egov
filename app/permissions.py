from fastapi import Depends, HTTPException, status

import app.config as config
import app.crud as crud
from app.repository import JWTBearer, JWTRepo


def get_token_data(token: str = Depends(JWTBearer())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = JWTRepo.decode_token(token)
    if token_data is None:
        raise credentials_exception
    return token_data


def access_for_manager(
    token_data: dict = Depends(get_token_data), db=Depends(config.get_db)
):
    user_email = token_data["sub"]
    existing_user = crud.get_user_by_email(db=db, email=user_email)
    if not existing_user or existing_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a manager",
        )
    return token_data


def access_for_standard_user(
    token_data: dict = Depends(get_token_data), db=Depends(config.get_db)
):
    user_email = token_data["sub"]
    existing_user = crud.get_user_by_email(db=db, email=user_email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found",
        )
    return token_data
