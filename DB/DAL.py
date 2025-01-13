#===============DB imports=============#
from DB.Pydantic_models import GAME_add_main_info, GAME_add_stats_info
from DB.session import get_db
from DB.SQL_models import Games_main_info, Games_static_info
from DB.ERRORS import GameAlreadyExistsError

#===============sqlalchemy imports=============#
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, insert


class DAL_games:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_game_main_info(self, game_data: GAME_add_main_info):
        game = Games_main_info(**game_data.model_dump())
        
        try:
            async with self.db() as session:
                async with session.begin():
                    session.add(game)
                await session.commit()
                return game
        except IntegrityError:
            raise GameAlreadyExistsError(name=game_data.name)

    async def add_game_static_info(self, game_data: GAME_add_stats_info):
        game_static_data = Games_static_info(**game_data.model_dump())
        statement = select(Games_static_info).where(Games_static_info.game_id == game_static_data.game_id)

        async with self.db() as session:
            async with session.begin():
                
                result = await session.execute(statement)
                existing_record = result.scalar_one_or_none()

                if existing_record is None:
                    session.add(game_static_data)
                    return game_static_data
                else:
                    if game_static_data.stars is not None:
                        existing_record.stars = game_static_data.stars
                    if game_static_data.players_total is not None:
                        existing_record.players_total = game_static_data.players_total
                    if game_static_data.players_online is not None:
                        existing_record.players_online = game_static_data.players_online
                    if game_static_data.production_date is not None:
                        existing_record.production_date = game_static_data.production_date
                    if game_static_data.current_version is not None:
                        existing_record.current_version = game_static_data.current_version
                    return game_static_data
                   
            await session.commit()