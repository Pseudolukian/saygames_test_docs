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
        return f"GameIdFieldRequireError: You dont enter game id parametr. "           