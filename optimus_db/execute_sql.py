from sqlalchemy import text, MetaData, Table
from db_connect import create_db_session

def execute_sql(sql_statement):

    # Execute the SQL statement
    with create_db_session() as session:
        result = session.execute(text(sql_statement))
        return result

def list_all_tables():
    with create_db_session() as session:
        # Create a MetaData instance
        meta = MetaData()

        # Reflect the tables
        meta.reflect(bind=session.get_bind())

        # Get the table names
        table_names = meta.tables.keys()
        print(f'Tables in your db:\n{list(table_names)}')


    return list(table_names)

def ask_and_drop_table(table_name):
    # Ask the user if they want to drop the table
    answer = input(f"Do you want to drop the table '{table_name}'? (y/n) ")
    if answer.lower() == 'y':
        with create_db_session() as session:
            # Create a MetaData instance
            meta = MetaData()

            # Reflect the tables
            meta.reflect(bind=session.get_bind())

            # If the table exists
            if table_name in meta.tables:
                # Get the table
                table = Table(table_name, meta)

                # Drop the table
                table.drop(bind=session.get_bind())

# Example usage:
if __name__ == "__main__":
    # List all tables
    result = list_all_tables()
    for row in result:
        table_name = row
        ask_and_drop_table(table_name)