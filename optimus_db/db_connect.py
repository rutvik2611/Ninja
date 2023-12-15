import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

load_dotenv()

def create_sqlalchemy_engine():
    """Create a new SQLAlchemy engine."""
    db_url = os.getenv("DATABASE_URL").replace("postgresql://", "cockroachdb://")
    engine = create_engine(db_url, echo=True)
    return engine

@contextmanager
def create_db_session(engine):
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

@contextmanager
def create_session_with_engine():
    """Create a new SQLAlchemy session with its own engine."""
    engine = create_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session