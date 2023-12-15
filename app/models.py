from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class RoleModel(BaseModel):
    id: int
    name: str


class UserModel(BaseModel):
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


class ModerationStatusEnum(str, Enum):
    APPROVED = "APPROVED"
    CANCELED = "CANCELED"
    ON_MODERATION = "ON_MODERATION"


class ModerationRequestModel(BaseModel):
    id: int
    user_id: int
    manager_id: int | None = None
    status: ModerationStatusEnum = ModerationStatusEnum.ON_MODERATION
    fields_to_change: dict
