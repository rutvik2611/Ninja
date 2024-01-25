from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, func, insert, update
from optimus_db.db_connect import create_db_session


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
    with create_db_session() as session:
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
    with create_db_session() as session:
        # Attempt to update the record for the user
        update_statement = update(r743189_table).where(r743189_table.c.user == user).values(rsa=rsa_value, time=func.now())
        result = session.execute(update_statement)

        if result.rowcount == 0:
            # If no rows were affected, print a message
            print(f"No record found for user: {user}")
        else:
            session.commit()

if __name__ == "__main__":

    with create_db_session() as session:
        metadata.create_all(session.get_bind())
        insert_rsa_value(12345678)
        update_rsa_value('r743189', 87654321)