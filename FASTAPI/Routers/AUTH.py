import sys
import os
from fastapi import APIRouter, Depends, HTTPException

root_path = os.path.abspath('/home/ubuntu/saygames')
sys.path.append(root_path)

from DB.session import get_db
from DB.DAL import AUTH
from DB.ERRORS import WrongUserUuidError
from DB.Pydantic_models import AUTH_api_token


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.get("/get_api_token", response_model=AUTH_api_token)
async def get_api_token(user_uuid:str):
    try:
        dal_auth = AUTH(db=get_db)
        response = await dal_auth.get_api_token(user_uuid=user_uuid)
    except WrongUserUuidError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response