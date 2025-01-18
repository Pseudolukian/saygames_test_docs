# user_uuid

API endpoint for retrieving the UUID of a user based on their credentials.

## Request Body

The request must include a JSON object with the following fields:

- **name** (string): The name of the user. (Required)
- **password** (string): The password of the user. (Required)

## Response

On success, returns a JSON object with the following field:

- **uuid** (string): The unique identifier (UUID) assigned to the user.

## Errors

Possible error responses include:

- **400 Bad Request**: If the provided username and password do not match any existing user, this error will be raised with a message indicating that the user UUID could not be found.