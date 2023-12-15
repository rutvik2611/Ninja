from sqlalchemy import update

from optimus_db.db_connect import create_session_with_engine
from optimus_db.secure_rsa_db.secure_rsa_db import secure_rsa

def update_attempt_status(new_status, msg=None):
    try:
        # Convert HTML to text
        with create_session_with_engine() as session:

            # Prepare the update statement
            stmt = update(secure_rsa).where(secure_rsa.c.valid == True).values(
                attempt_status=new_status,message=msg
            )

            # Execute the update statement
            session.execute(stmt)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_attempt_status("failure")