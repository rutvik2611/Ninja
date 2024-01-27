import json

from sqlalchemy import create_engine,text
import logging
from psycopg2 import connect

# from kai_lambda.python.sqlalchemy import text, create_engine

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Set up SQLAlchemy logger to use root logger
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.setLevel(logging.DEBUG)
sqlalchemy_logger.addHandler(logging.StreamHandler())



def create_sqlalchemy_postgres_engine():
    # Construct the connection string
    # db_url = "cockroachdb://others:5_r1eeRq1Bq0HnZLF3xkqg@bummed-walrus-13623.5xj.cockroachlabs.cloud:26257/ninja_db?sslmode=verify-full"
    db_url = "postgresql://nsgpuyes:uookN9JXE_2Exvk0SfvWr-7bw64zEiOr@kashin.db.elephantsql.com/nsgpuyes"
    logger.info(f"Connecting to: ")
    return create_engine(db_url, echo=True)

def lambda_handler(event, context):
    # Extract the 'user' and 'rsa' from the path parameters
    logger.info("Congratulations you in lambda_handler!")

    user = event['pathParameters']['user']
    rsa = event['pathParameters']['rsa']

    # Extract the query parameters
    # query_parameters = event.get('queryStringParameters', {})
    try:
        # Create the engine
        logger.info(f"User: {user}, RSA: {rsa}")
        engine = create_sqlalchemy_postgres_engine()
        logger.info("Engine created")


        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM r743189_table"))

        # Log the result
        logger.info(f"Query result: {result.fetchall()}")

        # Return a 200 OK response
        return {
            'statusCode': 200,
            'body': json.dumps(f'{user}:{rsa}:::Hello from Lambda!!')
        }
    except Exception as e:
        logger.debug("Error occurred while executing lambda function", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred: {}'.format(e))
        }

if __name__ == '__main__':
     # Set the logging level for the root logger to INFO
    logging.basicConfig(level=logging.INFO)
    # Test the lambda_handler function
    event = {
        'pathParameters': {
            'user': 'r743189',
            'rsa': '12344321'
        }
    }
    print(lambda_handler(event, None))