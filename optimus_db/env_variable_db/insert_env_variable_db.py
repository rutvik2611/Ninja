from sqlalchemy import insert
from optimus_db.db_connect import create_session_with_engine
from optimus_db.env_variable_db.env_variable_db import env_variables



# Create a session
with create_session_with_engine() as session:
    # Insert statement
    stmt = insert(env_variables).values(ninja_key='key1', ninja_value='value1')

    # Execute the statement
    session.execute(stmt)

    # Commit the transaction
    session.commit()