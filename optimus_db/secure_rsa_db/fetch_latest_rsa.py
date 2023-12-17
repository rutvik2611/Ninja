from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from optimus_db.db_connect import create_db_session
from optimus_db.secure_rsa_db.secure_rsa_db import secure_rsa


def fetch_valid_rsa_value():
    """Fetch the rsa_value of the row where valid is True."""
    # Create a session
    with create_db_session() as session:
        try:
            # Fetch the rsa_value of the valid row
            result = session.query(secure_rsa.c.rsa_value).filter_by(valid=True).one()

            return result[0]
        except NoResultFound:
            print("Error: No valid RSA value found in the database.")
        except MultipleResultsFound:
            print("Error: Multiple valid RSA values found in the database. There should be only one.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print(fetch_valid_rsa_value())