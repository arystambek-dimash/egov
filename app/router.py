from fastapi import APIRouter, Depends, HTTPException, Response, status
from passlib.context import CryptContext

import app.config as config
import app.crud as crud
from app.permissions import access_for_manager
from app.repository import JWTRepo
from app.schema import LoginSchema, SignUpSchema

router = APIRouter()

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpSchema, db=Depends(config.get_db)):
    existing_user = crud.get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    crud.create_user(db=db, user=user)
    return {"message": user}


@router.post("/login", status_code=status.HTTP_200_OK)
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


@router.get("/manager")
async def manager(cur_user: str = Depends(access_for_manager)):
    return {"message": "This is private data", "user": cur_user}
