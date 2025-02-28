from dotenv import load_dotenv
import os

from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, func, insert, update, create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

db_url = os.getenv("postgresql_connection")


# create a configured "Session" class
Session = sessionmaker(bind=create_engine(db_url, echo=True))

# create a Session
session = Session()

# Create a MetaData instance
metadata = MetaData()

# Create a table
r743189_table = Table(
   'r743189_table', metadata, 
   Column('user', String, default='r743189'), 
   Column('rsa', Integer), 
   Column('time', DateTime, default=func.now())
)



def insert_rsa_value(rsa_value):
    with Session() as session:
        # Check if a record already exists
        record = session.query(r743189_table).first()

        if record is None:
            # If no record exists, create a new one
            stmt = insert(r743189_table).values(rsa=rsa_value)
            session.execute(stmt)
        else:
            # If a record already exists, update it
            record.rsa = rsa_value
            session.commit()


def update_rsa_value(user, rsa_value):
    with Session() as session:
        # Attempt to update the record for the user
        update_statement = update(r743189_table).where(r743189_table.c.user == user).values(rsa=rsa_value, time=func.now())
        result = session.execute(update_statement)

        if result.rowcount == 0:
            # If no rows were affected, print a message
            print(f"No record found for user: {user}")
        else:
            session.commit()

def print_table():
    with Session() as session:
        # Fetch all records from the table
        records = session.query(r743189_table).all()

        # Print each record
        for record in records:
            print(f"User: {record.user}, RSA: {record.rsa}, Time: {record.time}")

def fetch_valid_rsa_postgres():
    """Fetch the rsa_value of the row where valid is True."""
    with Session() as session:
            record = session.query(r743189_table).first()
            if record is None:
                raise Exception("No RSA value found in the database.")
            else:
                return record.rsa,record.time


if __name__ == "__main__":


    with Session() as session:
    #     # metadata.create_all(session.get_bind())
    #     # insert_rsa_value(12345678)
    #     # update_rsa_value('r743189', 87654321)
        print(fetch_valid_rsa_postgres())
        print_table()
    # postgres_session()