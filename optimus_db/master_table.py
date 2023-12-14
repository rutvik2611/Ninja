from sqlalchemy import Table, Column, String, MetaData
from optimus_db.db_connect import db_session, c_engine

metadata = MetaData()

rp = Table(
   'rp', metadata,
   Column('user', String, primary_key=True),
   Column('secure_id', String),
   comment="This table holds users and their secure ids"
)

engine = c_engine()
with db_session(engine) as session:
    metadata.create_all(engine)



# Data to insert
data = [
    {"user": "user1", "secure_id": "id1"},
    {"user": "user2", "secure_id": "id2"},
    {"user": "user3", "secure_id": "id3"},
    {"user": "user4", "secure_id": "id4"},
    {"user": "user5", "secure_id": "id5"},
]

# Use the session in a context manager
with db_session(engine) as session:
    # Insert the data
    session.execute(rp.insert(), data)