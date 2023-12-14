from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr]
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]


class UserCreate(UserBase):
    pass


class UserRegistration(UserBase):
    password: str


class UserProfile(UserBase):
    id: int
    registered_at: Optional[datetime]

    class Config:
        datetime_format = "%Y-%m-%d"


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int
