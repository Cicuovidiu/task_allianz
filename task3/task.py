import requests
import json
import os

API_URL = "https://wps-interview.azurewebsites.net"
USERS_ENDPOINT = "/api/v1/user/"
ERROR_LOG_FILE = "error_log.json"

def get_users():
    response = requests.get(API_URL + USERS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch users (Status code: {response.status_code})")
        return []

def generate_email(user):
    firstname = user['firstname'].lower()
    lastname = user['lastname'].lower()

    if user.get('is_external'):
        return f"external_{lastname}.{firstname}@wps-allianz.de"
    else:
        return f"{firstname}.{lastname}@wps-allianz.de"

def update_user_email(user_id, updated_user_data):
    response = requests.put(f"{API_URL}{USERS_ENDPOINT}/{user_id}", json=updated_user_data)
    
    if response.status_code == 200:
        print(f"Successfully updated user ID {user_id} with email: {updated_user_data['email']}")
    else:
        print(f"Failed to update user ID {user_id} (Status code: {response.status_code})")

def log_error(user_id, generated_email):
    error_message = {
        "user_id": user_id,
        "error": f"Email {generated_email} already exists."
    }
    
    if os.path.exists(ERROR_LOG_FILE):
        with open(ERROR_LOG_FILE, 'r+') as log_file:
            data = json.load(log_file)
            data.append(error_message)
            log_file.seek(0)  # Move to the beginning of the file
            json.dump(data, log_file, indent=4)
    else:
        with open(ERROR_LOG_FILE, 'w') as log_file:
            json.dump([error_message], log_file, indent=4)

def filter_and_set_emails(user_list):
    #Use set to list only once the same accounts
    existing_emails = {user['email'] for user in user_list if user.get('email')}
    users_missing_email = [user_null_mail for user_null_mail in user_list if not user_null_mail.get('email')]

    for user_account in users_missing_email:
        generated_email = generate_email(user_account)

        if generated_email in existing_emails:
            log_error(user_account['id'], generated_email)
            print(f"Error: Email {generated_email} already exists for user ID {user_account['id']}.")
        else:
            user_account['email'] = generated_email
            existing_emails.add(generated_email)  # Update the set of existing emails
            update_user_email(user_account['id'], user_account)

    return user_list

def save_to_json(users, filename="error_user.json"):
    with open(filename, 'w') as f:
        json.dump(users, f, indent=4)
    print(f"Updated users saved to {filename}")

if __name__ == "__main__":
    users = get_users()
    if users:
        error_user = filter_and_set_emails(users)
        save_to_json(error_user)
    else:
        print("No users found or an error occurred while fetching users.")