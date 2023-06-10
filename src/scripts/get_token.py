import sys

import requests
import yaml


def get_user_token(email, password):
    with open('secrets/firebase.yml', 'r') as file:
        firebase_config = yaml.safe_load(file)

    api_key = firebase_config['apiKey']

    endpoint = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'
    payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }

    try:

        response = requests.post(endpoint, json=payload)
        response_data = response.json()

        if 'idToken' in response_data:
            return response_data['idToken']
        else:
            print('Error:', response_data.get('error', 'Unknown error'))
            return None
    except requests.exceptions.RequestException as e:
        print('Error making request:', str(e))
        return None


def main():
    if len(sys.argv) != 3:
        print("Use: python get_token.py [email] [password]")
        return

    email = sys.argv[1]
    password = sys.argv[2]

    user_token = get_user_token(email, password)
    if user_token:
        print("User token:", user_token)
    else:
        print("Unable to obtain user token.")


if __name__ == "__main__":
    main()
