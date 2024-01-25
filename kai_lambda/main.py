def lambda_handler(event, context):
    # Extract the 'user' and 'rsa' from the path parameters
    user = event['pathParameters']['user']
    rsa = event['pathParameters']['rsa']

    # TODO: Add your logic here to process the 'user' and 'rsa'

    # Return a 200 OK response
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!!')
    }