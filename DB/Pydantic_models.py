from pydantic import BaseModel, Field
from typing import Optional
import datetime

class GAME_add_main_info(BaseModel):
    name:            str                     = Field(..., min_length=3)
    genre:           Optional[str]           = Field(default = None)
    platform:        Optional[str]           = Field(default = None)
    developer:       Optional[str]           = Field(default = None)

class GAME_add_stats_info(BaseModel):
    game_id:         int                     = Field(...)
    stars:           Optional[int]           = Field(default = None)          
    players_total:   Optional[int]           = Field(default = None)          
    players_online:  Optional[int]           = Field(default = None)        
    production_date: Optional[datetime.date] = Field(default = None) #Format: yyyy-mm-dd | Separator: -
    current_version: Optional[str]           = Field(default = None)

#=================== Return data models =======================#
class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class GAME_success_addeded(TunedModel):
    game_name: str = None
    game_id: int = None
    status: str = Field(default="Game was added")
