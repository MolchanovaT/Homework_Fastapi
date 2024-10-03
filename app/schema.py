import datetime
import uuid
from typing import Literal

from pydantic import BaseModel


class IdReturnBase(BaseModel):
    id: int


class StatusSuccessBase(BaseModel):
    status: Literal["success"]


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime.datetime
    price: float
    user_id: int


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: float = 0


class CreateAdvertisementResponse(IdReturnBase):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class UpdateAdvertisementResponse(IdReturnBase):
    pass


class DeleteAdvertisementResponse(StatusSuccessBase):
    pass


class BaseUser(BaseModel):
    name: str
    password: str
    is_admin: bool


class LoginRequest(BaseUser):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID


class CreateUserRequest(BaseUser):
    pass


class CreateUserResponse(IdReturnBase):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str


class UpdateUserRequest(BaseModel):
    name: str | None = None


class UpdateUserResponse(IdReturnBase):
    pass


class DeleteUserResponse(StatusSuccessBase):
    pass
