import fastapi

import crud
import models
import schema
from constants import STATUS_SUCCESS_RESPONSE
from dependencies import SessionDependency
from lifespan import lifespan

app = fastapi.FastAPI(
    title="Test Application", version="0.0.1", description="...", lifespan=lifespan
)


@app.get("/v1/advertisement/{ad_id}", response_model=schema.GetAdvertisementResponse)
async def get_advertisement(ad_id: int, session: SessionDependency):
    ad = await crud.get_item(session, models.Advertisement, ad_id)
    return ad.dict


@app.post("/v1/advertisement", response_model=schema.CreateAdvertisementResponse)
async def create_advertisement(ad_json: schema.CreateAdvertisementRequest, session: SessionDependency):
    ad = models.Advertisement(**ad_json.dict())
    ad = await crud.add_item(session, ad)
    return ad.id_dict


@app.patch("/v1/advertisement/{ad_id}", response_model=schema.UpdateAdvertisementResponse)
async def update_advertisement(
        ad_id: int, ad_json: schema.UpdateAdvertisementRequest, session: SessionDependency
):
    ad = await crud.get_item(session, models.Advertisement, ad_id)
    ad_patch = ad_json.dict(exclude_unset=True)
    for field, value in ad_patch.items():
        setattr(ad, field, value)
    await crud.add_item(session, ad)
    return ad.id_dict


@app.delete("/v1/advertisement/{ad_id}", response_model=schema.DeleteAdvertisementResponse)
async def delete_advertisement(ad_id: int, session: SessionDependency):
    await crud.delete_item(session, models.Advertisement, ad_id)
    return STATUS_SUCCESS_RESPONSE


@app.get("/v1/user/{user_id}", response_model=schema.GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user = await crud.get_user(session, models.User, user_id)
    return user.dict


@app.post("/v1/user", response_model=schema.CreateUserResponse)
async def create_user(user_json: schema.CreateUserRequest, session: SessionDependency):
    user = models.User(**user_json.dict())
    user = await crud.add_user(session, user)
    return user.id_dict


@app.patch("/v1/user/{user_id}", response_model=schema.UpdateUserResponse)
async def update_user(
        user_id: int, user_json: schema.UpdateUserRequest, session: SessionDependency
):
    user = await crud.get_user(session, models.User, user_id)
    user_patch = user_json.dict(exclude_unset=True)
    for field, value in user_patch.items():
        setattr(user, field, value)
    await crud.add_user(session, user)
    return user.id_dict


@app.delete("/v1/user/{user_id}", response_model=schema.DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency):
    await crud.delete_user(session, models.User, user_id)
    return STATUS_SUCCESS_RESPONSE
