from sqlalchemy import insert

from optimus_db.env_variable_db.env_variable_db import env_variables


def load_env_variables():
    """Load environment variables from a .env file."""
    env_vars = {}

    # Open .env file
    with open('../.env') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value.strip("'\"")

    return env_vars


print(load_env_variables())


def insert_or_update_env_variables(env_vars):
    """Insert or update environment variables in the env_variables table."""

    # Create a session
    with create_db_session() as session:
        for ninja_key, ninja_value in env_vars.items():
            # Insert or update statement
            stmt = insert(env_variables).values(ninja_key=ninja_key, ninja_value=ninja_value)

            # Execute the statement
            session.execute(stmt)

        # Commit the transaction
        session.commit()


from sqlalchemy import delete
from optimus_db.db_connect import create_db_session


def delete_all_env_variables():
    """Delete all entries in the env_variables table."""

    # Create a session
    with create_db_session() as session:
        # Delete statement
        stmt = delete(env_variables)

        # Execute the statement
        session.execute(stmt)

        # Commit the transaction
        session.commit()

def insert_key_value(key, value):
    """Insert or update environment variables in the env_variables table."""

    # Create a session
    with create_db_session() as session:
        # Insert or update statement
        stmt = insert(env_variables).values(ninja_key=key, ninja_value=value)

        # Execute the statement
        session.execute(stmt)

    # Commit the transaction
    session.commit()


if __name__ == "__main__":
    insert_or_update_env_variables(load_env_variables())
    # delete_all_env_variables()
    pass
