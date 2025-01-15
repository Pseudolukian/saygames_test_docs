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

@game_router.post("/add_game", response_model = GAME_success_addeded_main_data)
async def add_game(add_game_main_data: GAME_add_main_info = Depends(GAME_add_main_info)):
    try:
        dal_games = DAL_games(db=get_db)
        added_game = await dal_games.add_game_main_info(game_data=add_game_main_data)
        response = GAME_success_addeded_main_data(game_name = added_game.name, game_id = added_game.id)
    except GameAlreadyExistsError as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    return response

@game_router.post("/add_game_static_info", response_model=GAME_success_addeded_static_info)
async def add_game_static_info(add_game_static_data: GAME_add_stats_info = Depends(GAME_add_stats_info)):
    try:
        dal_games = DAL_games(db=get_db)
        result = await dal_games.add_game_static_info(game_data=add_game_static_data)
        response = GAME_success_addeded_static_info(**result.model_dump())
    except GameIdNotFindError as err:
        raise HTTPException(status_code=400, detail=str(err))     
    return response

@game_router.get("/get_game_full_info", response_model = GAME_full_data_return)
async def get_game_full_info(get_id: GET_full_game_data = Depends(GET_full_game_data)):
    dal_games = DAL_games(db=get_db)
    result = await dal_games.get_full_game_data(game_id=get_id.game_id)
    response = GAME_full_data_return(**result.model_dump())
    return response

@game_router.get("/get_games_list", response_model = GAMES_list_return)
async def get_games_list(get_serch_list_params: GET_games_list = Depends(GET_games_list)):
    dal_games = DAL_games(db=get_db)
    result = await dal_games.get_games_list(req_type=get_serch_list_params.type, req_limit= get_serch_list_params.limit, req_offset= get_serch_list_params.offset)
    return result
