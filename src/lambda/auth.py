import json
import os

from firebase_admin import auth, credentials, initialize_app    # type: ignore


def lambda_handler(event, context):     # type: ignore

    secrets = os.environ["FIREBASE_CREDENTIALS"]
    config = json.loads(secrets)

    if 'authorizationToken' not in event:
        raise Exception('No auth token was provided')

    authorization_header = event['authorizationToken']
    try:
        authorization_token = authorization_header.split('Bearer ')[1]
    except Exception:
        raise Exception("No Bearer token provided")

    try:

        cred = credentials.Certificate(config)
        initialize_app(cred)

        decoded_token = auth.verify_id_token(authorization_token)
        auth_granted = True

    except Exception:
        decoded_token = None
        auth_granted = False

    return make_auth_response(decoded_token, event, auth_granted=auth_granted)


def make_auth_response(decoded_token, event, auth_granted=False):

    response = {
        'principalId': decoded_token["uid"] if auth_granted else '*',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow' if auth_granted else 'Deny',
                    'Resource': event['methodArn']
                }
            ]
        },
        'context': {
            'decodedToken': decoded_token if auth_granted else {}
        }
    }

    return response
