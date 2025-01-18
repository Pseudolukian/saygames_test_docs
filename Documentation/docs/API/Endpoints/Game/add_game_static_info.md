# add_game_static_info

API endpoint for adding static information about a game to the database.

## Request Body

The request must include the following fields in JSON format:

- **game_id** (integer): The unique identifier for the game. (Required)
- **stars** (integer, optional): The rating of the game, represented as stars. (1-5)
- **players_total** (integer, optional): The total number of players that can play the game.
- **players_online** (integer, optional): The current number of players online.
- **production_date** (string, optional): The date when the game was produced. Format: yyyy-mm-dd.
- **current_version** (string, optional): The current version of the game. Recommended format: vN.M (where N is the major version and M is the minor version).

## Response

On success, returns a JSON object with the following fields:

- **game_id** (integer): The unique identifier for the game.
- **stars** (integer, optional): The rating of the game.
- **players_total** (integer, optional): The total number of players for the game.
- **players_online** (integer, optional): The current number of players online.
- **production_date** (string, optional): The production date of the game.
- **current_version** (string, optional): The current version of the game.
- **status** (string): A message indicating that the static data was successfully added. Default is "Static data was successfully added."

## Errors

Possible error responses:

- **400 Bad Request**: If the specified game ID is not found in the database, this error will be raised with a message indicating that the game ID was not found.