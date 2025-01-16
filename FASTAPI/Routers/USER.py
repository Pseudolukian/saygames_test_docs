import sys
import os
from fastapi import APIRouter, Depends, HTTPException

root_path = os.path.abspath('/home/ubuntu/saygames')
sys.path.append(root_path)

from DB.Pydantic_models import USER_create, USER_success_created
from DB.DAL import USER
from DB.session import get_db


user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/add_user", response_model=USER_success_created)
async def add_user(user_data:USER_create = Depends(USER_create)):
    dal_user = USER(db=get_db)
    create_user = await dal_user.user_create(name = user_data.name, password = user_data.password)
    response = USER_success_created(uuid=create_user.uuid)
    return response