from sqlalchemy import MetaData, Table, Column, PrimaryKeyConstraint, Integer, DateTime, func
from optimus_db.db_connect import create_sqlalchemy_engine

# Create engine
engine = create_sqlalchemy_engine()

# Create a MetaData instance
metadata = MetaData()

# Create a table
secure_rsa = Table(
   'secure_rsa', metadata,
   Column('id', Integer, primary_key=True, autoincrement=True),
   Column('rsa_value', Integer),
   Column('time', DateTime, default=func.now(), onupdate=func.now())
)

# Create all tables in the metadata
metadata.create_all(engine)