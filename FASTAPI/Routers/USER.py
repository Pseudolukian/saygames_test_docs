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

add_user_router_info = """
API endpoint for adding a new user to the database.

### Request Body

The request must include a JSON object with the following fields:

- **name** (string): The name of the user. (Required)
- **password** (string): The password for the user. (Required)

### Response

On success, returns a JSON object with the following fields:

- **uuid** (string): The unique identifier (UUID) of the newly created user.
- **status** (string): A message indicating that the user has been successfully added. Default is "User added."

### Errors

Possible error responses include:

- **400 Bad Request**: This could occur if required fields are missing or invalid.
"""

@user_router.post("/add_user", response_model=USER_success_created, description=add_user_router_info)
async def add_user(user_data:USER_create = Depends(USER_create)):
    __doc__ = add_user_router_info
    dal_user = USER(db=get_db)
    create_user = await dal_user.user_create(name = user_data.name, password = user_data.password)
    response = USER_success_created(uuid=create_user.uuid)
    return response

get_user_uuid_router_info = """
API endpoint for retrieving the UUID of a user based on their credentials.

### Request Body

The request must include a JSON object with the following fields:

- **name** (string): The name of the user. (Required)
- **password** (string): The password of the user. (Required)

### Response

On success, returns a JSON object with the following field:

- **uuid** (string): The unique identifier (UUID) assigned to the user.

### Errors

Possible error responses include:

- **400 Bad Request**: If the provided username and password do not match any existing user, this error will be raised with a message indicating that the user UUID could not be found.
"""

@user_router.get("/user_uuid", response_model=USER_uuid, description=get_user_uuid_router_info)
async def get_user_uuid(user_data:USER_create = Depends(USER_create)):
    __doc__ = get_user_uuid_router_info
    try:
        dal_user = USER(db=get_db)
        user_uuid = await dal_user.user_get_uuid(user_name=user_data.name, user_password= user_data.password)
        response = USER_uuid(uuid=user_uuid)
        return response
    except UserGetUuidError as err:
        raise HTTPException(status_code=400, detail=str(err))