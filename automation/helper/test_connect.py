import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

print(os.environ["DATABASE_URL"])
db=os.environ["DATABASE_URL"]

db='postgresql://postgres:postgres@db.127.0.0.1.nip.io:5432/postgres'
engine = create_engine(db)
conn = engine.connect()

res = conn.execute(text("SELECT now()")).fetchall()
print(res)