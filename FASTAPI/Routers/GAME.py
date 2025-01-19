import sys
import os
from fastapi import APIRouter, Depends, HTTPException

root_path = os.path.abspath('/home/ubuntu/saygames')
sys.path.append(root_path)

from DB.Pydantic_models import *
from DB.DAL import DAL_games
from DB.ERRORS import GameAlreadyExistsError, GameIdNotFindError
from DB.session import get_db


game_router = APIRouter(prefix="/games", tags=["Game"])

add_game_router_info = """
API endpoint for adding a new game to the database.

### Request Body

The request must include the following fields in JSON format:

- **game_data**: An object containing the details of the game to be added.
    - **name** (string): The name of the game. (Required)
    - **type** (string): The genre of the game. Default is "action".
    - **platform** (string): The platform for which the game is developed. Default is "ios".
    - **developer** (string, optional): The name of the game's developer.

### Response

On success, returns a JSON object with the following fields:

- **game_id** (integer): The unique identifier for the newly added game.
- **game_name** (string): The name of the added game.
- **status** (string): A message indicating that the game was successfully added. Default is "Game was added."

### Errors

Possible error responses:

- **400 Bad Request**: If a game with the same name already exists in the database, this error will be raised with a message indicating that the game already exists.
- **404 Not Found**: If the specified game ID is not found in the database."""

@game_router.post("/add_game", response_model = GAME_success_addeded_main_data, description = add_game_router_info)

async def add_game(add_game_main_data: GAME_add_main_info = Depends(GAME_add_main_info), api_token:CHECK_Api_Token = Depends(CHECK_Api_Token)):
    __doc__ = add_game_router_info
    try:
        dal_games = DAL_games(db=get_db)
        added_game = await dal_games.add_game_main_info(game_data = add_game_main_data, api_token = api_token.api_token)
        
        response = GAME_success_addeded_main_data(game_name=added_game.game_name, game_id=added_game.game_id)
    except GameAlreadyExistsError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


add_game_static_info_router_info = """
API endpoint for adding static information about a game to the database.

### Request Body

The request must include the following fields in JSON format:

- **game_id** (integer): The unique identifier for the game. (Required)
- **stars** (integer, optional): The rating of the game, represented as stars. (1-5)
- **players_total** (integer, optional): The total number of players that can play the game.
- **players_online** (integer, optional): The current number of players online.
- **production_date** (string, optional): The date when the game was produced. Format: yyyy-mm-dd.
- **current_version** (string, optional): The current version of the game. Recommended format: vN.M (where N is the major version and M is the minor version).

### Response

On success, returns a JSON object with the following fields:

- **game_id** (integer): The unique identifier for the game.
- **stars** (integer, optional): The rating of the game.
- **players_total** (integer, optional): The total number of players for the game.
- **players_online** (integer, optional): The current number of players online.
- **production_date** (string, optional): The production date of the game.
- **current_version** (string, optional): The current version of the game.
- **status** (string): A message indicating that the static data was successfully added. Default is "Static data was successfully added."

### Errors

Possible error responses:

- **400 Bad Request**: If the specified game ID is not found in the database, this error will be raised with a message indicating that the game ID was not found.
"""

@game_router.post("/add_game_static_info", response_model=GAME_success_addeded_static_info, description = add_game_static_info_router_info)

async def add_game_static_info(add_game_static_data: GAME_add_stats_info = Depends(GAME_add_stats_info), api_token:CHECK_Api_Token = Depends(CHECK_Api_Token)):
    __doc__ = add_game_static_info_router_info
    try:
        dal_games = DAL_games(db=get_db)
        result = await dal_games.add_game_static_info(game_data=add_game_static_data, api_token = api_token.api_token)
        response = GAME_success_addeded_static_info(**result.model_dump())
    except GameIdNotFindError as err:
        raise HTTPException(status_code=400, detail=str(err))     
    return response

get_game_full_info_router_info = """
API endpoint for retrieving full information about a game based on its ID.

### Query Parameters

The request must include the following query parameter:

- **game_id** (integer): The unique identifier for the game. (Required)

### Response

On success, returns a JSON object with the following fields:

- **id** (integer, optional): The unique identifier for the record in the database.
- **game_id** (integer, optional): The unique identifier for the game.
- **name** (string, optional): The name of the game.
- **genre** (string, optional): The genre of the game (e.g., action, adventure).
- **platform** (string, optional): The platform on which the game is available (e.g., PC, console).
- **developer** (string, optional): The name of the developer of the game.
- **stars** (integer, optional): The rating of the game, represented as stars (1-5).
- **players_total** (integer, optional): The total number of players that can play the game.
- **players_online** (integer, optional): The current number of players online.
- **production_date** (string, optional): The production date of the game. Format: yyyy-mm-dd.
- **current_version** (string, optional): The current version of the game. Recommended format: vN.M (where N is the major version and M is the minor version).

### Errors

Possible error responses include:

- **404 Not Found**: If a game with the specified game ID does not exist in the database, this error will be raised indicating that the game was not found.
"""

@game_router.get("/get_game_full_info", response_model = GAME_full_data_return, description = get_game_full_info_router_info)

async def get_game_full_info(get_id: GET_full_game_data = Depends(GET_full_game_data), api_token:CHECK_Api_Token = Depends(CHECK_Api_Token)):
    __doc__ = get_game_full_info_router_info
    dal_games = DAL_games(db=get_db)
    result = await dal_games.get_full_game_data(game_id=get_id.game_id, api_token = api_token.api_token)
    response = GAME_full_data_return(**result.model_dump())
    return response

get_games_list_router_info = """
API endpoint for retrieving a list of games based on search parameters.

### Query Parameters

The request can include the following query parameters:

- **type** (string, optional): The genre or type of games to filter by (e.g., action, adventure).
- **limit** (integer, optional): The maximum number of games to return in the response. Default is 10.
- **offset** (integer, optional): The number of games to skip before starting to collect the result set. This is used for pagination. Default is 0.

### Response

On success, returns a JSON object with the following fields:

- **games** (array of objects): A list of games that match the search criteria. Each game object contains:
    - **id** (integer): The unique identifier for the game.
    - **game_id** (integer): The unique identifier for the game.
    - **name** (string): The name of the game.
    - **genre** (string): The genre of the game.
    - **platform** (string): The platform on which the game is available.
    - **developer** (string): The name of the developer of the game.
- **total** (integer): The total number of games that match the search criteria.
- **offset** (integer): The offset used in the request for pagination.
"""
@game_router.get("/get_games_list", response_model = GAMES_list_return, description = get_games_list_router_info)

async def get_games_list(get_serch_list_params: GET_games_list = Depends(GET_games_list), api_token:CHECK_Api_Token = Depends(CHECK_Api_Token)):
    __doc__ = get_games_list_router_info
    dal_games = DAL_games(db=get_db)
    result = await dal_games.get_games_list(req_type=get_serch_list_params.type, req_limit= get_serch_list_params.limit, req_offset= get_serch_list_params.offset, api_token = api_token.api_token)
    return result