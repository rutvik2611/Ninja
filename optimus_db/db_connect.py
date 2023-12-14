from dotenv import load_dotenv
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

from sqlalchemy.exc import DBAPIError
from contextlib import contextmanager
import os



def c_engine():
    """Create a new SQLAlchemy engine."""
    db = os.environ["DATABASE_URL"]
    engine = create_engine(db, echo=True)
    return engine

@contextmanager
def db_session(engine):
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

# Use the session in a context manager
# Create engine
# engine = c_engine()
# with db_session(engine) as session:
#     result = session.execute(text("SELECT now()"))
#     for row in result:
#         print(row)
