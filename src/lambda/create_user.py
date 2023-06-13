import json
import boto3
from botocore.exceptions import BotoCoreError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


def lambda_handler(event, context):

    body = json.loads(event['body'])
    user_id = body['uid']
    user_email = body['email']
    print(event)

    try:
        table.put_item(
            Item={
                'uid': user_id,
                'email': user_email
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully inserted item')
        }
    except BotoCoreError as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error inserting item')
        }
