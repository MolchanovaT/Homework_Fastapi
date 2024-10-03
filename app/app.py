import auth
import crud
import fastapi
import models
import schema
from constants import STATUS_SUCCESS_RESPONSE
from dependencies import SessionDependency, TokenDependency
from lifespan import lifespan
from sqlalchemy import select

app = fastapi.FastAPI(
    title="Test Application", version="0.0.1", description="...", lifespan=lifespan
)


@app.get("/v1/advertisement/{ad_id}", response_model=schema.GetAdvertisementResponse)
async def get_advertisement(ad_id: int, session: SessionDependency):
    ad = await crud.get_item(session, models.Advertisement, ad_id)
    return ad.dict


@app.post("/v1/advertisement", response_model=schema.CreateAdvertisementResponse)
async def create_advertisement(ad_json: schema.CreateAdvertisementRequest, session: SessionDependency,
                               token: TokenDependency):
    ad = models.Advertisement(**ad_json.dict(), user_id=token.user_id)
    await auth.check_access_rights(
        session, token, ad, write=True, read=False, raise_exception=True
    )
    ad = await crud.add_item(session, ad)
    return ad.id_dict


@app.patch("/v1/advertisement/{ad_id}", response_model=schema.UpdateAdvertisementResponse)
async def update_advertisement(
        ad_id: int, ad_json: schema.UpdateAdvertisementRequest, session: SessionDependency, token: TokenDependency
):
    ad = await crud.get_item(session, models.Advertisement, ad_id)
    await auth.check_access_rights(session, token, ad, write=True, read=False)
    ad_patch = ad_json.dict(exclude_unset=True)
    for field, value in ad_patch.items():
        setattr(ad, field, value)
    await crud.add_item(session, ad)
    return ad.id_dict


@app.delete("/v1/advertisement/{ad_id}", response_model=schema.DeleteAdvertisementResponse)
async def delete_advertisement(ad_id: int, session: SessionDependency, token: TokenDependency):
    ad = await crud.get_item(session, models.Advertisement, ad_id)
    await auth.check_access_rights(session, token, ad, write=True, read=False)
    await crud.delete_item(session, models.Advertisement, ad_id)
    return STATUS_SUCCESS_RESPONSE


@app.get("/v1/user/{user_id}", response_model=schema.GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user = await crud.get_item(session, models.User, user_id)
    return user.dict


@app.post("/v1/user", response_model=schema.CreateUserResponse)
async def create_user(user_data: schema.CreateUserRequest, session: SessionDependency):
    user = models.User(**user_data.dict())
    user.password = auth.hash_password(user_data.password)
    if user.is_admin:
        role = await auth.get_role(session, 'admin')
    else:
        role = await auth.get_role(session, 'user')
    user.roles = [role]
    await crud.add_item(session, user)

    return user.id_dict


@app.patch("/v1/user/{user_id}", response_model=schema.UpdateUserResponse)
async def update_user(
        user_id: int, user_json: schema.UpdateUserRequest, session: SessionDependency, token: TokenDependency
):
    user = await crud.get_item(session, models.User, user_id)
    await auth.check_access_rights(session, token, user, write=True, read=False)
    user_patch = user_json.dict(exclude_unset=True)
    if "password" in user_patch:
        user_patch["password"] = auth.hash_password(user_patch["password"])
    for field, value in user_patch.items():
        setattr(user, field, value)
    await crud.add_item(session, user)
    return user.id_dict


@app.delete("/v1/user/{user_id}", response_model=schema.DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user = await crud.get_item(session, models.User, user_id)
    await auth.check_access_rights(session, token, user, write=True, read=False)
    await crud.delete_item(session, models.User, user_id)
    return STATUS_SUCCESS_RESPONSE


@app.post("/v1/login", response_model=schema.LoginResponse)
async def login(login_data: schema.LoginRequest, session: SessionDependency):
    user_query = select(models.User).where(models.User.name == login_data.name)
    user_model = await session.scalar(user_query)
    if user_model is None:
        raise fastapi.HTTPException(401, "User or password is incorrect")
    if not auth.check_password(login_data.password, user_model.password):
        raise fastapi.HTTPException(401, "User or password is incorrect")

    token = models.Token(user_id=user_model.id)
    token = await crud.add_item(session, token)
    return {"token": token.token}
