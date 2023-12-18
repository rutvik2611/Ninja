from sqlalchemy import MetaData, Table, Column, String, PrimaryKeyConstraint
from optimus_db.db_connect import create_db_session


# Create a MetaData instance
metadata = MetaData()

# Create a table
env_variables = Table(
   'env_variables', metadata, 
   Column('ninja_key', String), 
   Column('ninja_value', String), 
   PrimaryKeyConstraint('ninja_key', name='ninja_key')
)

if __name__ == "__main__":
    with create_db_session() as session:
        metadata.create_all(session.get_bind())