from sqlalchemy import create_engine, text
from db_connect import create_sqlalchemy_engine, create_db_session

def execute_sql(sql_statement):
    # Create engine
    engine = create_sqlalchemy_engine()

    # Execute the SQL statement
    with create_db_session() as session:
        result = session.execute(text(sql_statement))
        session.commit()  # Commit the transaction
        return result

def list_all_tables():
    # SQL statement to get all table names
    sql_statement = '''
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public';
    '''
    result = execute_sql(sql_statement)
    return result

def ask_and_drop_table(table_name):
    # Ask the user if they want to drop the table
    answer = input(f"Do you want to drop the table '{table_name}'? (y/n) ")
    if answer.lower() == 'y':
        # SQL statement to drop the table
        sql_statement = f'DROP TABLE "{table_name}";'
        execute_sql(sql_statement)
        print(f"Table '{table_name}' dropped.")

# Example usage:
if __name__ == "__main__":
    # List all tables
    result = list_all_tables()
    for row in result:
        table_name = row[0]
        ask_and_drop_table(table_name)