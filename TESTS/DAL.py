import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_path)

from DB.session import get_db
from DB.Pydantic_models import GAME_add_main_info, GAME_add_stats_info
from DB.DAL import DAL_games, USER, AUTH
from data_tests import games_name, genre, platform, api_kokens
from random import randint
import random, string


async def auto_add_main_game_data():
    session = get_db
    dal = DAL_games(db=session)
    count = 0
    for name in games_name:
        input_data = GAME_add_main_info(name = name, genre = genre[randint(0,len(genre)-1)], 
                                        platform = platform[randint(0,len(platform)-1)],
                                        developer = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
        add_game_main_data = await dal.add_game_main_info(game_data=input_data, api_token = api_kokens["liquid"])
        count+=1
    return f"{count} games added to BD."

async def manual_add_main_game_data():
    session = get_db
    dal = DAL_games(db=session)
    input_data = GAME_add_main_info(name = "test_01", genre = genre[randint(0,len(genre)-1)], platform = platform[randint(0,len(platform)-1)], developer = "tester")
    add_game_main_data = await dal.add_game_main_info(game_data=input_data, api_token="eafcd723-44a7-3aef-9d57-e6eec77ecc5e")
    print(add_game_main_data)
    return f"Game {input_data.name} added to BD."

async def manual_add_static_game_info():
    session = get_db
    dal = DAL_games(db=session)
    imput_data = GAME_add_stats_info(game_id=70, players_online= 100)
    add_stats_game_info = await dal.add_game_static_info(game_data=imput_data, api_token = api_kokens["liquid"])
    print(add_stats_game_info)

async def automaic_add_static_games_info():
    session = get_db
    dal = DAL_games(db=session)
    ids = await dal.get_games_ids()
    for id in ids:
        gendata = GAME_add_stats_info(game_id=id, stars = random.randint(0,100), 
                                      players_total = random.randint(0,100),
                                      players_online = random.randint(0,100), 
                                      production_date = f"{random.randint(2020,2025)}-{random.randint(10,12)}-{random.randint(10,12)}",
                                      current_version=f"v{random.randint(1,20)}")
        await dal.add_game_static_info(game_data=gendata, api_token = api_kokens["liquid"])

async def get_full_game_data():
    session = get_db
    dal = DAL_games(db=session)
    full_game_data = await dal.get_full_game_data(game_id=70, api_token=api_kokens["liquid"])
    print(full_game_data)

async def get_full_games_list():
    session = get_db
    dal = DAL_games(db=session)
    games_list = await dal.get_games_list(api_token=api_kokens["liquid"], type = "Arcade", offset=0, limit=4)
    print(games_list)
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
    asyncio.run(get_full_games_list())