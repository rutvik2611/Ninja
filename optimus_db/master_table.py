from sqlalchemy import MetaData, Table, Column, String, PrimaryKeyConstraint
from db_connect import create_sqlalchemy_engine, create_session_with_engine

metadata = MetaData()

# Define the Ninja_ENV table
Ninja_ENV = Table(
   'Ninja_ENV', metadata,
   Column('ninja_key', String),
   Column('ninja_value', String),
   PrimaryKeyConstraint('ninja_key', name='ninja_key')
)

# Create the table in the database
engine = create_sqlalchemy_engine()
metadata.create_all(engine)

# Use the session in a context manager
with create_session_with_engine() as session:
    # You can now use the session to interact with the Ninja_ENV table
    pass