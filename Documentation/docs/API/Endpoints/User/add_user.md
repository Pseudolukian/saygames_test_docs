# add_user.md

API endpoint for adding a new user to the database.

## Request Body

The request must include a JSON object with the following fields:

- **name** (string): The name of the user. (Required)
- **password** (string): The password for the user. (Required)

## Response

On success, returns a JSON object with the following fields:

- **uuid** (string): The unique identifier (UUID) of the newly created user.
- **status** (string): A message indicating that the user has been successfully added. Default is "User added."

## Errors

Possible error responses include:

- **400 Bad Request**: This could occur if required fields are missing or invalid.