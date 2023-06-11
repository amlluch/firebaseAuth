import json
import os

from firebase_admin import auth, credentials, initialize_app    # type: ignore


secrets = os.environ["FIREBASE_CREDENTIALS"]
config = json.loads(secrets)

cred = credentials.Certificate(config)
initialize_app(cred)


def lambda_handler(event, context):     # type: ignore

    if 'authorizationToken' not in event:
        return make_auth_response(event)

    authorization_header = event['authorizationToken']
    try:
        authorization_token = authorization_header.split('Bearer ')[1]
    except Exception:
        return make_auth_response(event)

    try:
        decoded_token = auth.verify_id_token(authorization_token)
        auth_granted = True

    except Exception:
        decoded_token = None
        auth_granted = False

    return make_auth_response(event, decoded_token=decoded_token,  auth_granted=auth_granted)


def make_auth_response(event, decoded_token=None, auth_granted=False):

    if decoded_token is None:
        decoded_token = {}
    return {
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
            'decodedToken': json.dumps(decoded_token) if auth_granted else ""
        }
    }
