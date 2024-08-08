import requests
import random
import string
import threading
import time

def generate_token():
    email = get_temp_email()
    if not email:
        print("Failed to generate a temporary email.")
        return

    password = ''.join(random.choice(string.digits) for _ in range(10))
    username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))

    payload = {
        "captcha_key": None,
        "consent": True,
        "date_of_birth": "2000-01-01",
        "email": email,
        "fingerprint": "",
        "gift_code_sku_id": None,
        "invite": None,
        "password": password,
        "promotional_email_opt_in": True,
        "username": username
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://discord.com/api/v9/auth/register", json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            token = response.json().get("token")
            if token:
                print(f"Generated Token: {token}")
                join_server(token)
            else:
                print("Token not found in the response.")
        else:
            print(f"Error generating token: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while generating the token: {e}")

def join_server(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Joined server with token: {token}")
        else:
            print(f"Error joining server: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while joining the server: {e}")

def get_temp_email():
    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        response.raise_for_status()  # Check for HTTP errors

        # Debug output to understand the response
        print(f"Response content type: {response.headers.get('Content-Type')}")
        print(f"Response text: {response.text}")

        if 'application/json' in response.headers.get('Content-Type', ''):
            email_list = response.json()
            if email_list:
                return email_list[0]
            else:
                print("No email returned from the API.")
                return None
        else:
            print("Unexpected content type received.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting a temporary email: {e}")
        return None

def main():
    global invite_code
    invite_code = input("Discord Server Invite Link: ").split("/")[-1]

    try:
        response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")
        response.raise_for_status()
        print("Server exists.")
    except requests.exceptions.RequestException as e:
        print(f"Invalid server invite: {e}")
        return

    num_joins = int(input("Number of accounts to join: "))
    join_delay = float(input("Join delay (seconds): "))

    for _ in range(num_joins):
        thread = threading.Thread(target=generate_token)
        thread.start()
        time.sleep(join_delay)  # Set delay between account generations

if __name__ == "__main__":
    main()
