import psycopg2

def connect_to_db(db_config):
    """Establishes a connection to a PostgreSQL database."""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to database '{db_config.get('dbname')}': {e}")
        return None

def create_new_database(db_name):
    """
    TODO: Implement the logic to create a new empty database.
    """
    print(f"TODO: Create new empty database named '{db_name}'")