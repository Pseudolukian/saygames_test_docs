import sys
import os
from fastapi import APIRouter, Depends, HTTPException

root_path = os.path.abspath('/home/ubuntu/saygames')
sys.path.append(root_path)

from DB.Pydantic_models import USER_create, USER_success_created, USER_uuid
from DB.DAL import USER
from DB.session import get_db
from DB.ERRORS import UserGetUuidError


user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/add_user", response_model=USER_success_created)
async def add_user(user_data:USER_create = Depends(USER_create)):
    dal_user = USER(db=get_db)
    create_user = await dal_user.user_create(name = user_data.name, password = user_data.password)
    response = USER_success_created(uuid=create_user.uuid)
    return response

@user_router.get("/user_uuid", response_model=USER_uuid)
async def get_user_uuid(user_data:USER_create = Depends(USER_create)):
    try:
        dal_user = USER(db=get_db)
        user_uuid = await dal_user.user_get_uuid(user_name=user_data.name, user_password= user_data.password)
        response = USER_uuid(uuid=user_uuid)
        return response
    except UserGetUuidError as err:
        raise HTTPException(status_code=400, detail=str(err))