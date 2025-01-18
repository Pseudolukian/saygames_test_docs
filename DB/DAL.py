#===============DB imports=============#
from DB.session import get_db

#========= SQL Models ===========#
from DB.SQL_models import Games_main_info, Games_static_info, USER_data

#======== Errors ================#
from DB.ERRORS import GameAlreadyExistsError, GameIdNotFindError, GameIdFieldRequireError, UserGetUuidError, WrongUserUuidError, WrongApiTokenError

#========== Pydantic Models =====#
from DB.Pydantic_models import USER_data_add, USER_success_created, AUTH_api_token, GAME_success_addeded_main_data, GAME_add_stats_info, GAME_add_main_info, GAME_success_addeded_static_info, CHECK_Api_Token, GAME_full_data_return, GET_games_list, GAMES_list_return, GameGenre, GAME_short_data_return

#===============SQLalchemy imports=============#
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, insert, join

from pydantic_core import ValidationError


class DAL_games:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_game_main_info(self, game_data: GAME_add_main_info, api_token: CHECK_Api_Token) -> GAME_success_addeded_main_data:
        add_main_game_info = Games_main_info(**game_data.model_dump())
        try:
            async with self.db() as session:
                async with session.begin():
                    await AUTH.check_api_token(self, session=session, api_token=api_token)
                    session.add(add_main_game_info)
                    await session.flush()
                    
                    game_add_static_info = GAME_add_stats_info(game_id=add_main_game_info.id)
                    add_game_static_info = Games_static_info(**game_add_static_info.model_dump())
                    session.add(add_game_static_info)
                    
                    await session.commit()
        
        except IntegrityError:
            raise GameAlreadyExistsError(name=game_data.name)
        
        response = GAME_success_addeded_main_data(game_name=add_main_game_info.name, game_id=add_main_game_info.id)
        return response
    
    async def add_game_static_info(self, game_data: GAME_add_stats_info, api_token: CHECK_Api_Token) -> GAME_success_addeded_static_info:
        game_static_data = Games_static_info(**game_data.model_dump())
        statement = select(Games_static_info).where(Games_static_info.game_id == game_static_data.game_id)

        async with self.db() as session:
            async with session.begin():
                try:
                    await AUTH.check_api_token(self, session=session, api_token=api_token)
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
                
                
                updated_record = await session.execute(statement)
                updated_data = updated_record.scalar_one()
                await session.commit()
        
        request = GAME_success_addeded_static_info(**game_data.model_dump())
        return request.model_dump(exclude_none=True)
    
    async def get_full_game_data(self, game_id: int, api_token: CHECK_Api_Token) -> GAME_full_data_return:
        async with self.db() as session:
            async with session.begin():
                await AUTH.check_api_token(self, session=session, api_token=api_token)
                check_game_id_req = select(Games_main_info).where(Games_main_info.id == game_id)
                check_game_id_result = await session.execute(check_game_id_req)
                existing_record = check_game_id_result.scalar()
                if existing_record is not None:
                    statement = select(Games_main_info, Games_static_info).select_from(
                    join(Games_main_info, Games_static_info, Games_main_info.id == Games_static_info.game_id)
                    ).where(Games_main_info.id == game_id)
                else:
                    raise GameIdNotFindError(game_id=game_id)
            result = await session.execute(statement)
            final_result = GAME_full_data_return()

            for main_info, static_info in result.all():
                for field, value in main_info.model_dump().items():
                    setattr(final_result, field, value)
                for field, value in static_info.model_dump().items():
                    setattr(final_result, field, value)    
        return final_result
    
    async def get_games_list(self, api_token: CHECK_Api_Token, type:GameGenre, offset:int, limit:int) -> GAMES_list_return:
        get_game_list_params = GET_games_list(type=type, limit=limit, offset=offset)
        final_result = GAMES_list_return()
        async with self.db() as session:
            async with session.begin():
                await AUTH.check_api_token(self, session=session, api_token=api_token)
                request = (
                    select(Games_main_info)
                    .where(Games_main_info.genre == get_game_list_params.type)
                    .offset(get_game_list_params.offset)
                    .limit(get_game_list_params.limit)
                )
                result = await session.execute(request)
                games = result.all()
                final_result.games = [GAME_short_data_return(**game[0].model_dump()) for game in games]
                final_result.total = len(games)
                final_result.offset = get_game_list_params.offset
        return GAMES_list_return(games=final_result.games, total=final_result.total, offset=final_result.offset)

    async def get_games_ids(self) -> list[int]:
        request = select(Games_static_info.game_id)
        async with self.db() as session:
            async with session.begin():
                games_ids = await session.execute(request)
        return [id[0] for id in games_ids]



class USER:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def user_create(self, name: str, password: str):
        user_add_data = USER_data_add(name = name, password = password)

        req = insert(USER_data).values(**user_add_data.model_dump())
        
        
        async with self.db() as session:
            async with session.begin():
                await session.execute(req)
                await session.commit()
        
        final = USER_success_created(uuid=user_add_data.uuid)        
        return final
    
    async def user_get_uuid(self, user_name:str, user_password:str):
        req = select(USER_data).where(USER_data.name == user_name).where(USER_data.password == user_password)
        async with self.db() as session:
            async with session.begin():
                try:
                    response = await session.execute(req)
                    uuid = response.scalar().uuid
                except AttributeError:
                    raise UserGetUuidError(user_name=user_name)
        return uuid

class AUTH:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_api_token(self, user_uuid:str):
        req = select(USER_data).where(USER_data.uuid == user_uuid)
        async with self.db() as session:
            async with session.begin():
                try:
                    response = await session.execute(req)
                    api_token = response.scalar().api_token
                    final = AUTH_api_token(api_token=api_token)
                except AttributeError:
                    raise WrongUserUuidError
        return final
    
    async def check_api_token(self, session: AsyncSession, api_token: CHECK_Api_Token):
        req = select(USER_data).where(USER_data.api_token == api_token)
        result = await session.execute(req)
        user_data = result.scalars().all()
       
        if not user_data:
            raise WrongApiTokenError
