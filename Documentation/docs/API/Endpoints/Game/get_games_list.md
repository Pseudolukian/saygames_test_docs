# get_games_list

API endpoint for retrieving a list of games based on search parameters.

## Query Parameters

The request can include the following query parameters:

- **type** (string, optional): The genre or type of games to filter by (e.g., action, adventure).
- **limit** (integer, optional): The maximum number of games to return in the response. Default is 10.
- **offset** (integer, optional): The number of games to skip before starting to collect the result set. This is used for pagination. Default is 0.

## Response

On success, returns a JSON object with the following fields:

- **games** (array of objects): A list of games that match the search criteria. Each game object contains:
    - **id** (integer): The unique identifier for the game.
    - **game_id** (integer): The unique identifier for the game.
    - **name** (string): The name of the game.
    - **genre** (string): The genre of the game.
    - **platform** (string): The platform on which the game is available.
    - **developer** (string): The name of the developer of the game.
- **total** (integer): The total number of games that match the search criteria.
- **offset** (integer): The offset used in the request for pagination.