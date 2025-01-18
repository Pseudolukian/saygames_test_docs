# get_api_token

API endpoint for retrieving an API token based on the user UUID.

## Query Parameters

The request must include the following query parameter:

- **user_uuid** (string): The UUID of the user for whom the API token is being requested. (Required)

## Response

On success, returns a JSON object with the following field:

- **api_token** (string): The API token associated with the specified user.

## Errors

Possible error responses:

- **400 Bad Request**: If the provided user UUID does not match any existing user in the database, this error will be raised with a message indicating that an incorrect user UUID was provided.