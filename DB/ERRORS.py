class GameAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"AlreadyExistsError: Game with name '{self.name}' already exists in the database."