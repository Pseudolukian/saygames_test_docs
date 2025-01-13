import sys
import os
from fastapi import APIRouter, Depends, HTTPException
from DB.session import get_db

root_path = os.path.abspath('/home/ubuntu/saygames')
sys.path.append(root_path)

from DB.Pydantic_models import *
from DB.DAL import DAL_games
from DB.ERRORS import GameAlreadyExistsError

game_router = APIRouter()

@game_router.post("/add_game", response_model = GAME_success_addeded)
async def add_game(add_game_main_data: GAME_add_main_info = Depends(GAME_add_main_info)):
    try:
        dal_games = DAL_games(db=get_db)
        added_game = await dal_games.add_game_main_info(game_data=add_game_main_data)
        response = GAME_success_addeded(game_name = added_game.name, game_id = added_game.id)
    except GameAlreadyExistsError as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    return response

