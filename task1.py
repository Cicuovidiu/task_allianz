import requests
import json

API_URL = "https://wps-interview.azurewebsites.net"
USER_ENDPOINT = "/api/v1/user/"  

def get_users():
    # Fetch the users
    response = requests.get(API_URL + USER_ENDPOINT)
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error: Unable to fetch users (Status code: {response.status_code})")
        return []

def filter_users_without_email(users):
    # Filter users who do not have an email address set or have an empty email address
    users_without_email = [user for user in users if not user.get('email')]
    
    # Print each user found without an email
    for user in users_without_email:
        print(f"User with ID {user['id']} ({user['firstname']} {user['lastname']}) has a null email address")
    
    return users_without_email

def save_to_json(users, filename="null_mail_users.json"):
    # Save the filtered users to a JSON file
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)
    print(f"Users without email addresses saved to {filename}")

if __name__ == "__main__":
    users = get_users()
    if users:
        users_without_email = filter_users_without_email(users)
        save_to_json(users_without_email)
    else:
        print("No users found or an error occurred while fetching users.")