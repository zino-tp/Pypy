import requests
import random
import string
import threading
import time

def generate_token():
  email = get_temp_email()
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

  response = requests.post("https://discord.com/api/v9/auth/register", json=payload, headers=headers)

  if response.status_code == 201:
    token = response.json()["token"]
    print(f"Generated Token: {token}")
    join_server(token)
  else:
    print(f"Error generating token: {response.text}")

def join_server(token):
  headers = {
    "Authorization": token
  }

  response = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers)

  if response.status_code == 200:
    print(f"Joined server with token: {token}")
  else:
    print(f"Error joining server: {response.text}")

def get_temp_email():
  response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
  email = response.json()[0]
  return email

def main():
  global invite_code
  invite_code = input("Discord Server Invite Link: ").split("/")[-1]

  try:
    requests.get(f"https://discord.com/api/v9/invites/{invite_code}")
    print("Server exists.")
  except:
    print("Invalid server invite.")
    return

  num_joins = int(input("Number of accounts to join: "))
  join_delay = float(input("Join delay (seconds): "))

  for _ in range(num_joins):
    thread = threading.Thread(target=generate_token)
    thread.start()
    time.sleep(join_delay)

if __name__ == "__main__":
  main()
 
