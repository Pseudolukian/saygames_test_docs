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

get_api_token_router_info = """
API endpoint for retrieving an API token based on the user UUID.

### Query Parameters

The request must include the following query parameter:

- **user_uuid** (string): The UUID of the user for whom the API token is being requested. (Required)

### Response

On success, returns a JSON object with the following field:

- **api_token** (string): The API token associated with the specified user.

### Errors

Possible error responses:

- **400 Bad Request**: If the provided user UUID does not match any existing user in the database, this error will be raised with a message indicating that an incorrect user UUID was provided.
"""

@auth_router.get("/get_api_token", response_model=AUTH_api_token, description = get_api_token_router_info)
async def get_api_token(user_uuid:str):
    __doc__ = get_api_token_router_info
    try:
        dal_auth = AUTH(db=get_db)
        response = await dal_auth.get_api_token(user_uuid=user_uuid)
    except WrongUserUuidError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response