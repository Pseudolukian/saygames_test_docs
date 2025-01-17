from typing import Optional
from sqlmodel import Field, SQLModel, UUID
import datetime

class Games_main_info(SQLModel, table=True):
    __tablename__ = 'games_main_info'
    id:              int                     = Field(primary_key = True, nullable = False, unique = True)
    name:            str                     = Field(nullable = False, unique = True)
    genre:           Optional[str]           = Field(nullable = True)
    platform:        Optional[str]           = Field(nullable = True)
    developer:       Optional[str]           = Field(nullable = True)

class Games_static_info(SQLModel, table=True):
    __tablename__ = 'games_static_info'
    game_id:         int                     = Field(primary_key = True, nullable = False, unique = True, foreign_key="games_main_info.id")
    stars:           Optional[int]           = Field(nullable = True)          
    players_total:   Optional[int]           = Field(nullable = True)          
    players_online:  Optional[int]           = Field(nullable = True)        
    production_date: Optional[datetime.date] = Field(nullable = True)
    current_version: Optional[str]           = Field(nullable = True)

class USER_data(SQLModel, table=True):
    __tablename__ = 'saygames_users'
    id:             int                      = Field(primary_key=True, nullable=False, unique=True)
    uuid:           str                     = Field(nullable=False, unique=True)
    name:           str                      = Field(nullable=False, unique= True)
    password:       str                      = Field(nullable=False)
    api_token:      Optional[str]           = Field(default=None)
