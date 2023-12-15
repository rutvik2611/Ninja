from sqlalchemy import Text,Time,Date,MetaData, Table, Column, PrimaryKeyConstraint, Integer, DateTime, func, Boolean
from optimus_db.db_connect import create_sqlalchemy_engine

# Create engine
engine = create_sqlalchemy_engine()

# Create a MetaData instance
metadata = MetaData()

secure_rsa = Table(
   'secure_rsa', metadata,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('rsa_value', Integer),
   Column('valid', Boolean, default=True),
   Column('attempt_status', Boolean, default=False),
   Column('date', Date, default=func.current_date()),
   Column('time', Time, default=func.current_time()),
   Column('datetime', DateTime, default=func.now(), onupdate=func.now()),
   # Column('html_content', Text, default='<html></html>')
)

# Create all tables in the metadata
metadata.create_all(engine)