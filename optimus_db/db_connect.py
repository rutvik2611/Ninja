import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

load_dotenv()

def create_sqlalchemy_engine():
    """Create a new SQLAlchemy engine."""

    # Load environment variables
    host = os.getenv("host")
    database_name = os.getenv("database_name")
    port = os.getenv("port")
    user = os.getenv("user")
    password = os.getenv("password")
    security = os.getenv("security")
    connection = os.getenv("connection")


    # Construct the connection string
    db_url = f"{connection}://{user}:{password}@{host}:{port}/{database_name}?{security}"

    if os.getenv("DATABASE_URL") != "":
        db_url = os.getenv("DATABASE_URL")

    db_url = db_url+"&sslrootcert=system"
    engine = create_engine(db_url, echo=False)
    return engine

# Create the engine at the module level
engine = create_sqlalchemy_engine()
print(f"Congratulations, you have connected to the database! @ {engine}")

@contextmanager
def create_db_session():
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    except DBAPIError:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":

    # Use the session in a context manager
    with create_db_session(engine) as session:
        result = session.execute(text("SELECT now()"))
        for row in result:
            print(row)
        print(f"Congratulations, you have connected to the database! @ {engine}")