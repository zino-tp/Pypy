import requests
import random
import string
import threading
import time

log_file = 'log.txt'

def write_log(message):
    with open(log_file, 'a') as f:
        f.write(message + '\n')

def generate_token():
    email = get_temp_email()
    if not email:
        write_log("Failed to generate a temporary email.")
        return

    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
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

    attempt = 0
    while attempt < 5:  # Maximal 5 Versuche
        try:
            response = requests.post("https://discord.com/api/v9/auth/register", json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                token = response.json().get("token")
                if token:
                    join_result = join_server(token)
                    write_log(f"Generated Token: {token} | Username: {username} | Password: {password} | Join Result: {join_result}")
                else:
                    write_log("Token not found in the response.")
                return
            else:
                write_log(f"Error generating token: {response.text}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                write_log("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)  # Warte 60 Sekunden bevor du es erneut versuchst
            else:
                write_log(f"An HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            write_log(f"An error occurred while generating the token: {e}")
        attempt += 1

    write_log("Failed to generate a token after multiple attempts.")

def join_server(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return "Joined successfully"
        else:
            return f"Error joining server: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while joining the server: {e}"

def get_temp_email():
    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        response.raise_for_status()  # Check for HTTP errors

        if 'application/json' in response.headers.get('Content-Type', ''):
            email_list = response.json()
            if email_list:
                return email_list[0]
            else:
                write_log("No email returned from the API.")
                return None
        else:
            write_log("Unexpected content type received.")
            return None
    except requests.exceptions.RequestException as e:
        write_log(f"An error occurred while getting a temporary email: {e}")
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

    print("All registration threads have been started.")
    write_log("All registration threads have been started.")

if __name__ == "__main__":
    main()
