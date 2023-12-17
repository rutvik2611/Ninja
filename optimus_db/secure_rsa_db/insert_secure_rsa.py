from sqlalchemy.exc import SQLAlchemyError
from optimus_db.db_connect import create_db_session
from optimus_db.secure_rsa_db.secure_rsa_db import secure_rsa


def insert_secure_rsa_1(rsa_value):
    """Insert a value into the secure_rsa table."""
    # Create a session
    with create_db_session() as session:
        try:
            # Insert the value
            session.execute(secure_rsa.insert().values(rsa_value=rsa_value))

            # Commit the transaction
            session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred while inserting value in rsa at python level: {e}")
            session.rollback()

def add_secure_rsa(rsa_value):
    """Add a new secure_rsa row and set the previous valid row to invalid."""
    # Create a session
    with create_db_session() as session:
        try:
            # Find the current valid row and set it to invalid
            session.query(secure_rsa).filter_by(valid=True).update({secure_rsa.c.valid: False})

            # Add a new row with the given rsa_value and set it to valid
            session.execute(secure_rsa.insert().values(rsa_value=rsa_value, valid=True))

            # Commit the transaction
            session.commit()
        except Exception as e:
            # Roll back the transaction
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            # Close the session
            session.close()

if __name__ == "__main__":
    insert_secure_rsa_1("83053322")
    add_secure_rsa("83053322")