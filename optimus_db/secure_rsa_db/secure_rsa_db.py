from sqlalchemy import String,Text,Time,Date,MetaData, Table, Column, PrimaryKeyConstraint, Integer, DateTime, func, Boolean
from optimus_db.db_connect import create_db_session



# Create a MetaData instance
metadata = MetaData()

secure_rsa = Table(
   'secure_rsa', metadata,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('rsa_value', Integer),
   Column('valid', Boolean, default=True),
   Column('attempt_status', String(10)),
   Column('date', Date, default=func.current_date()),
   Column('time', Time, default=func.current_time()),
   Column('datetime', DateTime, default=func.now(), onupdate=func.now()),
   Column('message', Text),
)

# Create all tables in the metadata
if __name__ == "__main__":
   # Create all tables in the metadata
   with create_db_session() as session:
      metadata.create_all(session.get_bind())