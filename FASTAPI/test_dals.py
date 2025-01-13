from DB.DAL.GAMES.DAL_games import DAL_games
from DB.session import get_db
from DATA_models.GAMES  import GAMECreateMain

dal_games = DAL_games(db=get_db)

dal_games.add_game(game_data=)