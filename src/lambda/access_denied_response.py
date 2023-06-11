import json
import boto3


def lambda_handler(event, context):
    print('REQUEST RECEIVED:\n' + json.dumps(event))

    api_gateway = boto3.client('apigateway')

    params = {
      'responseType': event['ResourceProperties']['ResponseType'],
      'restApiId': event['ResourceProperties']['RestApiId'],
      'statusCode': str(event['ResourceProperties']['StatusCode']),
      'responseParameters': {
        'gatewayresponse.header.Access-Control-Allow-Origin': "'*'",
        'gatewayresponse.header.Access-Control-Allow-Headers': "'*'"
      },
      'responseTemplates': event['ResourceProperties']['ResponseTemplates']
    }

    print('Updating Gateway Response with parameters: ' + json.dumps(params))

    try:
      response = api_gateway.put_gateway_response(**params)
      print('Success, response: ' + json.dumps(response))
    except Exception as error:
      print('Error: ' + str(error))
      raise error

    print('Sending response...')
    return send_response(event, context.log_stream_name, 'SUCCESS')

def send_response(event, log_stream_name, response_status, response_data=None):
    response_body = json.dumps({
      'Status': response_status,
      'Reason': 'See the details in CloudWatch Log Stream: ' + log_stream_name,
      'PhysicalResourceId': log_stream_name,
      'StackId': event['StackId'],
      'RequestId': event['RequestId'],
      'LogicalResourceId': event['LogicalResourceId'],
      'Data': response_data,
    })

    print('RESPONSE BODY:\n', response_body)
    return response_body
