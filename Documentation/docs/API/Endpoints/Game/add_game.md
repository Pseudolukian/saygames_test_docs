# add_game

API endpoint for adding a new game to the database.

## Request Body

The request must include the following fields in JSON format:

- **game_data**: An object containing the details of the game to be added.
    - **name** (string): The name of the game. (Required)
    - **type** (string): The genre of the game. Default is "action".
    - **platform** (string): The platform for which the game is developed. Default is "ios".
    - **developer** (string, optional): The name of the game's developer.

## Response

On success, returns a JSON object with the following fields:

- **game_id** (integer): The unique identifier for the newly added game.
- **game_name** (string): The name of the added game.
- **status** (string): A message indicating that the game was successfully added. Default is "Game was added."

## Errors

Possible error responses:

- **400 Bad Request**: If a game with the same name already exists in the database, this error will be raised with a message indicating that the game already exists.
- **404 Not Found**: If the specified game ID is not found in the database."""