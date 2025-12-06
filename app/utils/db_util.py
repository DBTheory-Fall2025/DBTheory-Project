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

def get_schema(conn):
    """Fetches the schema of the connected database."""
    schema = {}
    cursor = conn.cursor()
    try:
        # Get DB name for logging
        try:
            dsn_params = conn.get_dsn_parameters()
            db_name = dsn_params.get('dbname', 'unknown')
        except Exception:
            db_name = 'unknown'
            
        print(f"[DEBUG] get_schema: Connected to '{db_name}'", flush=True)

        # Get all tables in the public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"[DEBUG] get_schema: Found tables in public schema for '{db_name}': {tables}", flush=True)
        
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

def read_sql_data(conn, query, params=None):
    """Executes a read-only (SELECT) SQL query."""
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if cursor.description:
            return cursor.fetchall()
        return None
    except Exception as e:
        print(f"Error executing read query '{query}': {e}")
        raise
    finally:
        cursor.close()

def write_to_target_db(conn, query, params=None):
    """Executes a write (CREATE, INSERT, etc.) SQL query on the target DB."""
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        print(f"Executed write query: {query}")
    except Exception as e:
        print(f"Error executing write query '{query}': {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
