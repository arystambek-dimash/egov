from datetime import datetime

from pydantic import BaseModel


class Role(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    email: str
    phone_number: str
    first_name: str
    last_name: str
    address: str
    password: str
    registered_at: datetime
    role_id: int
    telegram_chat_id: str
