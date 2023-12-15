from sqlalchemy.exc import SQLAlchemyError

from optimus_db.db_connect import create_session_with_engine
from optimus_db.secure_rsa_db.secure_rsa_db import secure_rsa


def insert_secure_rsa(rsa_value):
    """Insert a value into the secure_rsa table."""
    # Create a session
    with create_session_with_engine() as session:
        try:
            # Insert the value
            session.execute(secure_rsa.insert().values(rsa_value=rsa_value))

            # Commit the transaction
            session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred while inserting value in rsa at python level: {e}")
            session.rollback()

if __name__ == "__main__":
    insert_secure_rsa("12343000")