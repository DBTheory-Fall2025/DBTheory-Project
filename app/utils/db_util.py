import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connect_to_db(db_config, db_name=None):
    """Establishes a connection to a PostgreSQL database."""
    config = db_config.copy()
    if db_name:
        config['dbname'] = db_name
    try:
        conn = psycopg2.connect(**config)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Could not connect to database '{config.get('dbname')}': {e}")
        return None

def create_new_database(db_config, db_name):
    """Creates a new empty database."""
    # Connect to the default 'postgres' database to run the CREATE DATABASE command
    conn = connect_to_db(db_config, db_name='postgres')
    if not conn:
        raise Exception("Could not connect to postgres database to create new database.")
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"An error occurred during database creation: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_schema(conn):
    """Fetches the schema of the connected database."""
    schema = {}
    cursor = conn.cursor()
    try:
        # Get all tables in the public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        for table_name in tables:
            # Get all columns for each table
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
            """, (table_name,))
            columns = {row[0]: row[1] for row in cursor.fetchall()}
            schema[table_name] = columns
            
        return schema
    finally:
        cursor.close()

def execute_query(conn, query, params=None):
    """Executes a given SQL query."""
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        print(f"Executed query: {query}")
        # If it's a SELECT query, you might want to fetch results
        if cursor.description:
            return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query '{query}': {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
