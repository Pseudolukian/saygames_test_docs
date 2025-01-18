class GameAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"AlreadyExistsError: Game with name '{self.name}' already exists in the database."

class GameIdNotFindError(Exception):
    def __init__(self, game_id: int):
        self.game_id = game_id

    def __str__(self):
        return f"GameIdNotFindError: Game with id {self.game_id} not find in the database." 

class GameIdFieldRequireError(Exception):
    def __str__(self):
        return f"GameIdFieldRequireError: You dont enter game id parametr."

class UserGetUuidError(Exception):
    def __init__(self, user_name):
        self.user_name = user_name
    
    def __str__(self):
        return f"User uuid assigned with username {self.user_name} does not find." 

class WrongUserUuidError(Exception):
    
    def __str__(self):
        return f"You input wrong iser uuid."      

class WrongApiTokenError(Exception):
    
    def __str__(self):
        return f"Wrong API-token."          