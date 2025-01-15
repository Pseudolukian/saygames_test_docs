#===============DB imports=============#
from DB.Pydantic_models import GAME_add_main_info, GAME_add_stats_info, GAME_full_data_return, GET_games_list, GAMES_list_return, GAME_short_data_return
from DB.session import get_db
from DB.SQL_models import Games_main_info, Games_static_info
from DB.ERRORS import GameAlreadyExistsError, GameIdNotFindError, GameIdFieldRequireError

#===============sqlalchemy imports=============#
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, insert, join

from pydantic_core import ValidationError


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
                try:
                    request = await session.execute(statement)
                    existing_record = request.scalar_one_or_none()
                    for field, value in game_static_data.model_dump().items():
                        if value is None:
                            setattr(game_static_data, field, getattr(existing_record, field))
                    if existing_record is None:
                        raise GameIdNotFindError(game_id = game_data.game_id)
                except ValidationError as e:
                    if any(error['loc'] == ('game_id',) for error in e.errors()):
                        raise GameIdFieldRequireError

                update_stmt = (
                    update(Games_static_info)
                    .where(Games_static_info.game_id == game_static_data.game_id)
                    .values(**game_static_data.model_dump())
                )
                await session.execute(update_stmt)
                await session.commit()
        return game_static_data
    
    async def get_full_game_data(self, game_id: int):
        async with self.db() as session:
            async with session.begin():
                statement = select(Games_main_info, Games_static_info).select_from(
                join(Games_main_info, Games_static_info, Games_main_info.id == Games_static_info.game_id)
                ).where(Games_main_info.id == game_id)

            result = await session.execute(statement)
            final_result = GAME_full_data_return()

            for main_info, static_info in result.all():
                for field, value in main_info.model_dump().items():
                    setattr(final_result, field, value)
                for field, value in static_info.model_dump().items():
                    setattr(final_result, field, value)    
        return final_result
    
    async def get_games_list(self, req_type: str, req_limit: int = 10, req_offset: int = 0):
        final_result = GAMES_list_return()
        async with self.db() as session:
            async with session.begin():
                request = (
                    select(Games_main_info)
                    .where(Games_main_info.genre == req_type)
                    .limit(req_limit)
                    .offset(req_offset)
                )
                result = await session.execute(request)
                games = result.all()
                final_result.games = [GAME_short_data_return(**game[0].model_dump()) for game in games]
                final_result.total = len(games)
                final_result.offset = req_offset
        return final_result
