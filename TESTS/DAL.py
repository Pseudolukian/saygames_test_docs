import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_path)

from DB.session import get_db
from DB.Pydantic_models import GAME_add_main_info, GAME_add_stats_info
from DB.DAL import DAL_games, USER, AUTH
from data_tests import games_name, genre, platform
from random import randint
import random, string


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

async def get_uuid_user():
    session = get_db
    dal = USER(db=session)
    uuid = await dal.user_get_uuid(user_name="pynanist", user_password="sukablanaxuy")
    print(uuid)
    return uuid

async def get_api_token():
    session = get_db
    dal = AUTH(db=session)
    api_token = await dal.get_api_token(user_uuid="ca0b9e92-d40b-11ef-92ca-edb0d1")
    print(api_token)
    return api_token

if __name__ == '__main__':
    asyncio.run(get_api_token())