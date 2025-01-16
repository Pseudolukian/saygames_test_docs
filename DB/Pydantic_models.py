from pydantic import BaseModel, Field
from typing import Optional
from typing import List
from uuid import UUID, uuid3, uuid1, NAMESPACE_DNS
import datetime
from enum import Enum

#===================== Lists =====================================#

class GameGenre(str, Enum):
    arcade = "Arcade"
    clicker = "Clicker"
    slasher = "Slasher"
    simulation = "Simulation"
    puzzle = "Puzzle"
    battle_royale = "Battle Royale"
    platformer = "Platformer"
    word = "Word"
    trivia = "Trivia"
    runner = "Runner"
    action = "Action"
    time_management = "Time Management"
    survival = "Survival"

class Platform(str, Enum):
    ios = "iOS"
    android = "Android"

#================================== Request data models ==========================#

class GAME_add_main_info(BaseModel):
    name:            str                     = Field(..., min_length=3)
    type:            GameGenre               = Field(default = GameGenre.action, description="The genre type of the game.")
    platform:        Platform                = Field(default=Platform.ios, description="The game platform")
    developer:       Optional[str]           = Field(default = None)

class GAME_add_stats_info(BaseModel):
    game_id:         int                     = Field(...)
    stars:           Optional[int]           = Field(default = None)          
    players_total:   Optional[int]           = Field(default = None)          
    players_online:  Optional[int]           = Field(default = None)        
    production_date: Optional[datetime.date] = Field(default = None, description="Data format: yyyy-mm-dd. Separator: -")
    current_version: Optional[str]           = Field(default = None, description="Recomended format: vN.M: N - major ver, M - minor ver.")


class GET_full_game_data(BaseModel):
    game_id:         int                     = Field(...)

class GET_games_list(BaseModel):
    type: GameGenre = Field(..., description="The genre type of the game.")
    limit: Optional[int] = Field(default=10, description="The maximum number of games to return.")
    offset: Optional[int] = Field(default=0, description="The number of records to skip.")


class USER_create(BaseModel):
    name:           str                      = Field(...)
    password:       str                      = Field(...)

class USER_data_add(USER_create):
    uuid:           str                     = Field(default_factory=lambda: str(uuid1()))
    api_token:      str                     = Field(default_factory=lambda: str(uuid3(NAMESPACE_DNS, "UUID_generic")))

#=================== Return data models =======================#
class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class GAME_success_addeded_main_data(TunedModel):
    game_name: str = None
    game_id: int = None
    status: str = Field(default="Game was added.")

class GAME_success_addeded_static_info(TunedModel, GAME_add_stats_info):
    status: str = Field(default="Static data was succesed added.")

class GAME_full_data_return(TunedModel):
    id:              Optional[int]           = Field(default = None)
    game_id:         Optional[int]           = Field(default = None)
    name:            Optional[str]           = Field(default = None)
    genre:           Optional[str]           = Field(default = None)
    platform:        Optional[str]           = Field(default = None)
    developer:       Optional[str]           = Field(default = None)
    stars:           Optional[int]           = Field(default = None)          
    players_total:   Optional[int]           = Field(default = None)          
    players_online:  Optional[int]           = Field(default = None)        
    production_date: Optional[datetime.date] = Field(default = None)
    current_version: Optional[str]           = Field(default = None)

class GAME_short_data_return(TunedModel):
    id:              Optional[int]           = Field(default = None)
    name:            Optional[str]           = Field(default = None)
    genre:           Optional[str]           = Field(default = None)


class GAMES_list_return(TunedModel):
    games: List[GAME_short_data_return] = Field(default_factory=list)
    total: int = Field(default=0)
    offset: int = Field(default=0)

class USER_success_created(TunedModel):
    uuid: UUID  = Field(default= None)
    status: str = Field(default="User addeded.")