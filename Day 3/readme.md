# Profile Functionality Expansion

## Changes Made

### 1. Model Changes

- Added a unique constraint on the `name` field in the `Profile` model to ensure each profile has a unique name.
- Included additional fields such as 'address' and 'mobile_number' in the `Profile` model.


### 2. Implemented a New Endpoint to Get Profile by Name

- Created a new view function `get_profile_by_name` in `views.py` to retrieve a profile by name and return the data in JSON format.
- Used the `Profile` model with proper error handling to respond with an appropriate status if the profile is not found.
- Updated the `urls.py` to include the new endpoint.


### 3. Implemented a New Endpoint to Update Email Address

- Created a new view function `update_email` in `views.py` to update the email address of a profile based on the provided name.
- Added validations to ensure the 'email' field is present in the request data, and provided appropriate error responses for missing or invalid data.
- Updated the `urls.py` to include the new endpoint.


## Challenges Faced

- Ensuring the unique constraint on the `name` field works correctly required careful consideration of the model structure and running migrations.

- Handling the retrieval of profiles by name in the `get_profile_by_name` view posed a challenge, requiring proper error handling and responding with appropriate HTTP statuses.

- Testing the `update_email` endpoint proved challenging, particularly due to complexities in simulating various scenarios. Comprehensive testing was essential to ensure the endpoint worked as expected under different conditions, and it required alot of attention to detail.
