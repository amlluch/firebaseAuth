import json
import boto3
from botocore.exceptions import BotoCoreError


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    body = json.loads(event['body'])
    user_id = body['uid']
    user_email = body['email']

    try:
        response = table.put_item(
            Item={
                'user_id': user_id,
                'email': user_email
            }
        )
        print(f'Successfully inserted item: {response}')
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully inserted item')
        }
    except BotoCoreError as e:
        print(f'Error inserting item: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Error inserting item')
        }
