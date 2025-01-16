import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_path)

from DB.session import get_db
from DB.Pydantic_models import GAME_add_main_info, GAME_add_stats_info
from DB.DAL import DAL_games, USER
from data_tests import games_name, genre, platform
from random import randint
import random, string

test_data_input_games = [
 GAME_add_main_info(name = "test_game", genre = "FPS", developer = "Me", platform = "iOS"),
 GAME_add_stats_info(game_id=1, players_total= 10, players_online= 15, production_date="2024-10-13", current_version="v1.2")
]


async def add_data():
    session = get_db
    dal = DAL_games(db=session)
    count = 0
    for name in games_name:
        input_data = GAME_add_main_info(name = name, genre = genre[randint(0,len(genre)-1)], 
                                        platform = platform[randint(0,len(platform)-1)],
                                        developer = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
        add_game_main_data = await dal.add_game_main_info(game_data=input_data)
        count+=1
    return f"{count} games added to BD."

async def get_full_games_list():
    session = get_db
    dal = DAL_games(db=session)
    games_list = await dal.get_games_list(req_type = "Slasher")
    return games_list

async def create_user():
    session = get_db
    dal = USER(db=session)
    cr_user = await dal.user_create(name="pynanist", password="sukablanaxuy")
    return cr_user

if __name__ == '__main__':
    asyncio.run(create_user())