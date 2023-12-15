from typing import Optional

from pydantic import BaseModel, EmailStr


class SignUpSchema(BaseModel):
    email: EmailStr
    phone_number: str
    first_name: Optional[str] = "RomanPostav69.5pzh"
    last_name: Optional[str] = "MneNuzhnaStipendiaRealno"
    address: Optional[str] = None
    password: Optional[str] = None
    telegram_chat_id: Optional[str] = None


class LoginSchema(BaseModel):
    email: EmailStr = "tima@1fit.app"
    password: str = "1FIT2021"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
