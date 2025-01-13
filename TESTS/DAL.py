import sys
import os
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_path)

from DB.session import get_db
from DB.Pydantic_models import GAME_add_main_info, GAME_add_stats_info
from DB.DAL import DAL_games

test_data =[
 GAME_add_main_info(name = "test_game", genre = "FPS", developer = "Me", platform = "iOS"),
 GAME_add_stats_info(game_id=1, stars=20, players_total= 20, players_online= 10, production_date="2024-10-13", current_version="v1.0")
]


async def main():
    session = get_db
    dal = DAL_games(db=session)
    #add_game = await dal.add_game_main_info(game_data=test_data[0])
    add_game_static_data = await dal.add_game_static_info(game_data=test_data[1])
    print(add_game_static_data)


if __name__ == '__main__':
    asyncio.run(main())