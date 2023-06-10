import sys

import firebase_admin
from firebase_admin import auth, credentials

from src.common import load_config

config = load_config()

cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred)


def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
        )
        print("User successfully created")
    except Exception as e:
        print(str(e))


def main():
    if len(sys.argv) != 3:
        print("Use: python create_user.py [email] [password]")
        return

    email = sys.argv[1]
    password = sys.argv[2]

    create_user(email, password)


if __name__ == "__main__":
    main()

