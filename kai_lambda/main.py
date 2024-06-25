import json


import logging
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime, func, update, Text, select, \
    desc

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

# Create the table
text_entry = Table(
    'text_entry',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('content', Text),
)

def encode_newlines(text):
    # Encode newlines as "\n" before JSON serialization
    return text.replace('\n', '\\n')

def decode_newlines(text):
    # Decode "\n" as newlines when displaying in the browser
    return text.replace('\\n', '\n')

def create_table(engine, table):
    # Create the table if it does not exist
    if not engine.dialect.has_table(engine.connect(), table.name):
        logger.info(f"Creating table: {table.name}")
        table.create(engine)

def get_latest_text_from_database():
    with engine.connect() as connection:
        query = select(text_entry.c.content).order_by(desc(text_entry.c.id)).limit(1)
        latest_text_entry = connection.execute(query).fetchone()
        connection.commit()
        return latest_text_entry[0] if latest_text_entry else None




def create_sqlalchemy_postgres_engine():
    # Construct the connection string 
    db_url = "postgresql://nsgpuyes:X5u5tFR4AehB0dkvfv4wJA6xhFlYUxwO@kashin.db.elephantsql.com/nsgpuyes"
    logger.debug(f"Connecting to: ")
    return create_engine(db_url, echo=False)

engine = create_sqlalchemy_postgres_engine()

## Create tables if they do not exist
# create_table(engine, r743189_table)
# create_table(engine, text_entry)



def lambda_handler(event, context):
    # Extract the 'user' and 'rsa' from the path parameters
    logger.debug("Congratulations you in lambda_handler!")

    userx = event['pathParameters']['user']
    rsax = event['pathParameters']['rsa']

    if userx == "get":
        latest_text = get_latest_text_from_database()
        if latest_text:
            # Encode newlines before JSON serialization
            response_body = decode_newlines(latest_text)
        else:
            response_body = "{}"  # Return empty JSON object if latest_text is empty

        return {
            'statusCode': 200,
            'body': response_body
        }

    # Extract the query parameters
    # query_parameters = event.get('queryStringParameters', {})
    try:
        # Create the engine
        logger.info(f"User: {userx}, RSA: {rsax}")

        logger.debug("Engine created")

        with engine.connect() as connection:
            

            update_statement = update(r743189_table).where(r743189_table.c.user == userx).values(rsa=rsax, time=func.now())
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
            'rsa': '0032132'
        }
    }
    print(lambda_handler(event, None))

    # # Test the lambda_handler function for retrieving the latest text entry
    event_get_text = {
         'pathParameters': {
             'user': 'get',
             'rsa': 'dummy'
         }
     }
    print(lambda_handler(event_get_text, None))


    # def validate_db_connection(engine):
    #
    #     # Establish a connection to the database
    #     with engine.connect() as connection:
    #         # Execute a simple query to validate the connection
    #         result = connection.execute(select(text_entry).order_by(desc(text_entry.c.id)).limit(1))
    #         # Fetch the result (optional)
    #         connection.commit()
    #         print(result.rowcount)
    #         print(result)
    #         # Log the successful validation
    #         logger.info("Database connection validated successfully.")
    #         # Return True to indicate successful validation
    #         return True
    #
    #
    # validate_db_connection(engine)
