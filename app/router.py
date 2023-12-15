from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from passlib.context import CryptContext
from starlette import schemas

import app.config as config
import app.crud as crud
import app.models as models
from app.permissions import (
    access_only_manager,
    access_only_standard_user,
    only_authorized_user,
)
from app.repository import JWTRepo
from app.schema import LoginSchema, ModerationRequestCreate, ProfileSchema, SignUpSchema

router = APIRouter()

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpSchema, db=Depends(config.get_db)):
    existing_user = crud.get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    crud.create_user(db=db, user=user)
    return {"message": user}


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(request: LoginSchema, db=Depends(config.get_db)):
    try:
        existing_user = crud.get_user_by_email(db=db, email=request.email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )

        if not pwd_context.verify(request.password, existing_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        token = JWTRepo.generate_token({"sub": request.email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as error:
        error_message = str(error.args)
        return Response(error_message, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/profile/", response_model=ProfileSchema, status_code=status.HTTP_200_OK)
async def profile(user: models.UserModel = Depends(only_authorized_user)):
    return ProfileSchema(**dict(user))


@router.post("/moderation/create/", status_code=status.HTTP_201_CREATED)
async def moderation_create(
    moderation_request: ModerationRequestCreate,
    user: models.UserModel = Depends(access_only_standard_user),
    db=Depends(config.get_db),
):
    moderation_request._user_id = user.id
    created_moderation_request = crud.create_moderation_request(
        moderation_request=moderation_request, db=db
    )
    return created_moderation_request


@router.get("/moderation/", status_code=status.HTTP_200_OK)
async def moderation_list(
    user: models.UserModel = Depends(access_only_manager),
    db=Depends(config.get_db),
):
    return crud.get_moderation_requests(db=db)


@router.get("/moderation/{moderation_request_id}", status_code=status.HTTP_200_OK)
async def moderation_list(
    moderation_request_id: int,
    user: models.UserModel = Depends(access_only_manager),
    db=Depends(config.get_db),
):
    return crud.get_moderation_request_by_id(
        db=db, moderation_request_id=moderation_request_id
    )


@router.post(
    "/moderation/{moderation_request_id}/approve/", status_code=status.HTTP_201_CREATED
)
async def moderation_approve(
    moderation_request_id: int,
    user: models.UserModel = Depends(access_only_manager),
    db=Depends(config.get_db),
):
    return crud.approve_moderation_request_by_id(
        db=db, moderation_request_id=moderation_request_id, user=user
    )


@router.post(
    "/moderation/{moderation_request_id}/cancel/", status_code=status.HTTP_201_CREATED
)
async def moderation_approve(
    moderation_request_id: int,
    user: models.UserModel = Depends(access_only_manager),
    db=Depends(config.get_db),
):
    return crud.cancel_moderation_request_by_id(
        db=db, moderation_request_id=moderation_request_id, user=user
    )
