import sys

import firebase_admin   # type: ignore
from firebase_admin import auth, credentials

from common import load_config

config = load_config()

cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred)


def verify_and_decode_custom_token(custom_token):
    try:
        decoded_token = auth.verify_id_token(custom_token)

        return decoded_token
    except Exception as e:
        print('Error verifying and decoding custom token:', str(e))
        return None


def main():
    if len(sys.argv) != 2:
        print("Use: python auth_token [token]")
        return

    token = sys.argv[1]

    jwt_data = verify_and_decode_custom_token(token)
    print(jwt_data)


if __name__ == "__main__":
    main()

