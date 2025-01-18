# get_game_full_info
API endpoint for retrieving full information about a game based on its ID.

### Query Parameters

The request must include the following query parameter:

- **game_id** (integer): The unique identifier for the game. (Required)

### Response

On success, returns a JSON object with the following fields:

- **id** (integer, optional): The unique identifier for the record in the database.
- **game_id** (integer, optional): The unique identifier for the game.
- **name** (string, optional): The name of the game.
- **genre** (string, optional): The genre of the game (e.g., action, adventure).
- **platform** (string, optional): The platform on which the game is available (e.g., PC, console).
- **developer** (string, optional): The name of the developer of the game.
- **stars** (integer, optional): The rating of the game, represented as stars (1-5).
- **players_total** (integer, optional): The total number of players that can play the game.
- **players_online** (integer, optional): The current number of players online.
- **production_date** (string, optional): The production date of the game. Format: yyyy-mm-dd.
- **current_version** (string, optional): The current version of the game. Recommended format: vN.M (where N is the major version and M is the minor version).

### Errors

Possible error responses include:

- **404 Not Found**: If a game with the specified game ID does not exist in the database, this error will be raised indicating that the game was not found.