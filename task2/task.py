import requests
import json

# Simple Configuration: Define your API URL and endpoint
API_URL = "https://wps-interview.azurewebsites.net"
USERS_ENDPOINT = "/api/v1/user/"

def get_users():
    # Properly construct the complete URL for the API request
    response = requests.get(API_URL + USERS_ENDPOINT)
    if response.status_code == 200:
        return response.json()  # Assuming the response is in JSON format
    else:
        print(f"Error: Unable to fetch users (Status code: {response.status_code})")
        return []

def generate_email(user):
    # Generate email based on whether the user is internal or external
    firstname = user['firstname'].lower()
    lastname = user['lastname'].lower()

    if user.get('is_external'):
        # External user
        return f"external_{lastname}.{firstname}@wps-allianz.de"
    else:
        # Internal user
        return f"{firstname}.{lastname}@wps-allianz.de"

def update_user_email(user_id, updated_user_data):
    # Update the user with the generated email
    response = requests.put(f"{API_URL}{USERS_ENDPOINT}/{user_id}", json=updated_user_data)
    
    if response.status_code == 200:
        print(f"Successfully updated user ID {user_id} with email: {updated_user_data['email']}")
    else:
        print(f"Failed to update user ID {user_id} (Status code: {response.status_code})")

def filter_and_set_emails(users):
    users_without_email = [user for user in users if not user.get('email')]

    # Process each user found without an email
    for user in users_without_email:
        # Generate email
        generated_email = generate_email(user)
        
        # Update user data with the generated email
        user['email'] = generated_email

        # Update the user in the database
        update_user_email(user['id'], user)

    return users

def save_to_json(users, filename="updated_users.json"):
    # Save the updated users to a JSON file
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)
    print(f"Updated users saved to {filename}")

if __name__ == "__main__":
    # Main workflow
    users = get_users()
    if users:
        updated_users = filter_and_set_emails(users)
        save_to_json(updated_users)
    else:
        print("No users found or an error occurred while fetching users.")