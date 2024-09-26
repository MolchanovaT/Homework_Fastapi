import datetime
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
    user_id: int


class CreateAdvertisementResponse(IdReturnBase):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    user_id: int | None = None


class UpdateAdvertisementResponse(IdReturnBase):
    pass


class DeleteAdvertisementResponse(StatusSuccessBase):
    pass


class GetUserResponse(BaseModel):

    id: int
    name: str


class CreateUserRequest(BaseModel):
    name: str


class CreateUserResponse(IdReturnBase):
    pass


class UpdateUserRequest(BaseModel):
    name: str | None = None


class UpdateUserResponse(IdReturnBase):
    pass


class DeleteUserResponse(StatusSuccessBase):
    pass
