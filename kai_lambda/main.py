import json

from sqlalchemy import create_engine



def create_sqlalchemy_postgres_engine():
    # Construct the connection string
    db_url = "cockroachdb://others:5_r1eeRq1Bq0HnZLF3xkqg@bummed-walrus-13623.5xj.cockroachlabs.cloud:26257/ninja_db?sslmode=verify-full"

    db_url = db_url + "&sslrootcert=system"
    engine = create_engine(db_url, echo=True)
    return engine
def lambda_handler(event, context):
    # Extract the 'user' and 'rsa' from the path parameters
    user = event['pathParameters']['user']
    rsa = event['pathParameters']['rsa']

    # Extract the query parameters
    query_parameters = event.get('queryStringParameters', {})

    # Create the engine at the module level
    engine = create_sqlalchemy_postgres_engine()
    print(f"Congratulations, you have connected to the database! @ {engine}")



    # TODO: Add your logic here to process the 'user', 'rsa', and query parameters

    # Return a 200 OK response
    return {
        'statusCode': 200,
        'body': json.dumps(f'{user}:{rsa}:{query_parameters}:{engine}:Hello from Lambda!!')
    }

if __name__ == '__main__':
    # Test the lambda_handler function
    event = {
        'pathParameters': {
            'user': 'r743189',
            'rsa': '12344321'
        }
    }
    print(lambda_handler(event, None))