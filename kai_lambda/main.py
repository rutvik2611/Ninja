import json


import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime, func, update 


# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configure logging to log to CloudWatch Logs
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Create a MetaData instance
metadata = MetaData()

# Create a table
r743189_table = Table(
   'r743189_table', metadata,
   Column('user', String, default='r743189'),
   Column('rsa', Integer),
   Column('time', DateTime, default=func.now())
)



def create_sqlalchemy_postgres_engine():
    # Construct the connection string 
    db_url = os.getenv("postgresql_connection")
    logger.debug(f"Connecting to: ")
    return create_engine(db_url, echo=False)

engine = create_sqlalchemy_postgres_engine()



def lambda_handler(event, context):
    # Extract the 'user' and 'rsa' from the path parameters
    logger.debug("Congratulations you in lambda_handler!")

    userx = event['pathParameters']['user']
    rsax = event['pathParameters']['rsa']

    # Extract the query parameters
    # query_parameters = event.get('queryStringParameters', {})
    try:
        # Create the engine
        logger.debug(f"User: {userx}, RSA: {rsax}")

        logger.debug("Engine created")

        with engine.connect() as connection:
            

            update_statement = update(r743189_table).where(r743189_table.c.user == userx).values(rsa=rsax)
            result = connection.execute(update_statement)

            # Get the number of rows that were updated
            # updated_rows = result.rowcount
            # logger.info(f"Number of rows updated: {updated_rows}")

            # get the first record from the table
            # select_statement = select(r743189_table.c.user, r743189_table.c.rsa).where(r743189_table.c.user == userx)
            # result = connection.execute(select_statement)
            # first_record = result.fetchone()
            # logger.info(f"Query result: {first_record}")
            

            connection.commit()




            
        # Log the result
        # logger.info(f"Query result: {first_record}")

        # Return a 200 OK response
        return {
            'statusCode': 200,
            'body': json.dumps(f'Update your rsa value for {userx}:{rsax}')
        }
    except Exception as e:
        logger.error("Error occurred while executing lambda function")
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
            'rsa': '12332132'
        }
    }
    print(lambda_handler(event, None))