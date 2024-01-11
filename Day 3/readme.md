# Django Profile Functionality Expansion

This project involves expanding the functionality of a Django project with a `Profile` model. Below are the steps taken to address the outlined requirements.

## Changes Made

### 1. Added Unique Constraint and Additional Fields in Profile Model

- In `models.py`, added a unique constraint on the `name` field and included additional fields like `address` and `mobile_number`.
- Applied migrations to update the database.

### 2. Implemented a New Endpoint to Retrieve a Single Profile by Name

- Added a new view function `get_profile_by_name` in `views.py` to retrieve a profile by name and return the data in JSON format.
- Updated `urls.py` to include the new endpoint.

### 3. Implemented a New Endpoint to Update an Email Address

- Added a new view function `update_email` in `views.py` to handle email updates.
- Updated `urls.py` to include the new email update endpoint.

## Challenges Faced

The challenges encountered during this assignment included:

1. **Adding Unique Constraint:** Ensuring the correct implementation of a unique constraint on the `name` field required careful consideration of the Django model.

2. **JSON Response Handling:** Managing JSON responses and error handling in the view functions to provide meaningful feedback to clients.

3. **Testing and Debugging:** Ensuring proper testing of each endpoint and debugging any issues that arose during development. In the end, tests to update the email did not take place.

Overall, the assignment provided valuable experience in extending Django functionality and handling data through API endpoints.

