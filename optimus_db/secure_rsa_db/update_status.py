from sqlalchemy import update
from bs4 import BeautifulSoup

from optimus_db.db_connect import create_session_with_engine
from optimus_db.secure_rsa_db.secure_rsa_db import secure_rsa

def update_attempt_status_and_html(new_status):
    try:
        # Convert HTML to text
        with create_session_with_engine() as session:
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()
            print(f'THIS  :{text_content}')

            # Prepare the update statement
            stmt = update(secure_rsa).where(secure_rsa.c.valid == True).values(
                attempt_status=new_status,
                html_content=text_content
            )

            # Execute the update statement
            session.execute(stmt)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_attempt_status_and_html(True, '''<html><head><title>Test</title></head><body><p>Test</p></body></html>''')