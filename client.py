import requests
import json

BASE_URL = "http://localhost:8000"


def register_user(username, password):
    """
    Registers a new user with the Polly API.

    Args:
        username (str): The username to register.
        password (str): The password for the new user.

    Returns:
        requests.Response: The response object from the API call, or None if a connection error occurs.
    """
    url = f"{BASE_URL}/register"
    user_data = {"username": username, "password": password}

    try:
        # Using the `json` parameter automatically sets the Content-Type header to application/json
        response = requests.post(url, json=user_data)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        # Return the response object even on HTTP error to allow for inspection of the body
        return http_err.response
    except requests.exceptions.RequestException as e:
        # For connection errors, etc.
        print(f"An error occurred during the request: {e}")
        return None


def get_polls(skip: int = 0, limit: int = 10):
    """
    Fetches a paginated list of polls.

    Args:
        skip (int): The number of polls to skip.
        limit (int): The maximum number of polls to return.

    Returns:
        requests.Response: The response object from the API call, or None if an error occurs.
    """
    url = f"{BASE_URL}/polls"
    params = {"skip": skip, "limit": limit}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return http_err.response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None


if __name__ == "__main__":
    # Example of how to use the function.
    # You can run this script directly to test user registration.
    new_username = "testuser"
    new_password = "a-very-secret-password"

    print(f"Attempting to register user '{new_username}'...")

    registration_response = register_user(new_username, new_password)

    if registration_response is not None:
        print(f"Status Code: {registration_response.status_code}")

        # Check if the request was successful (status code 2xx)
        if registration_response.ok:
            print("Registration successful!")
            try:
                print("Response JSON:", registration_response.json())
            except json.JSONDecodeError:
                print("Could not decode JSON from response.")
                print("Response Content:", registration_response.text)
        else:
            print("Registration failed.")
            try:
                # Attempt to print the JSON error message from the API
                print("Error Response:", registration_response.json())
            except json.JSONDecodeError:
                print("Could not decode JSON from error response.")
                print("Error Content:", registration_response.text)
    else:
        print("The request failed. Unable to get a response from the server.")

    # Example of fetching polls
    print("\nFetching polls...")
    polls_response = get_polls(skip=0, limit=10)

    if polls_response is not None:
        print(f"Status Code: {polls_response.status_code}")

        if polls_response.ok:
            print("Successfully fetched polls!")
            try:
                polls_data = polls_response.json()
                print("Polls Data:")
                # Pretty print the JSON
                print(json.dumps(polls_data, indent=2))
            except json.JSONDecodeError:
                print("Could not decode JSON from response.")
                print("Response Content:", polls_response.text)
        else:
            print("Failed to fetch polls.")
            try:
                print("Error Response:", polls_response.json())
            except json.JSONDecodeError:
                print("Could not decode JSON from error response.")
                print("Error Content:", polls_response.text)
    else:
        print("The request failed. Unable to get a response from the server.")
