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
    """Fetches the schema of the connected database (Simple version for backward compatibility)."""
    # This now just wraps the enhanced version and simplifies the output
    enhanced = get_enhanced_schema(conn)
    simple_schema = {}
    for table, details in enhanced.items():
        simple_schema[table] = details['columns']
    return simple_schema

def get_enhanced_schema(conn):
    """Fetches the schema of the connected database including PKs and FKs."""
    schema = {}
    cursor = conn.cursor()
    try:
        # Get DB name for logging
        try:
            dsn_params = conn.get_dsn_parameters()
            db_name = dsn_params.get('dbname', 'unknown')
        except Exception:
            db_name = 'unknown'
            
        print(f"[DEBUG] get_enhanced_schema: Connected to '{db_name}'", flush=True)

        # Get all tables in the public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"[DEBUG] get_enhanced_schema: Found tables in public schema for '{db_name}': {tables}", flush=True)
        
        for table_name in tables:
            # Get all columns for each table
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
            """, (table_name,))
            columns = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Get Primary Keys
            cursor.execute("""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                WHERE tc.table_name = %s 
                  AND tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_schema = 'public'
            """, (table_name,))
            pks = [row[0] for row in cursor.fetchall()]
            
            # Get Foreign Keys
            cursor.execute("""
                SELECT kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu 
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu 
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                  AND tc.table_name = %s
                  AND tc.table_schema = 'public'
            """, (table_name,))
            fks = [{'col': row[0], 'ref_table': row[1], 'ref_col': row[2]} for row in cursor.fetchall()]
            
            schema[table_name] = {
                'columns': columns,
                'pks': pks,
                'fks': fks
            }
            
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

def read_sql_data_with_headers(conn, query, params=None):
    """Executes a read-only query and returns (columns, rows)."""
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return {'columns': columns, 'rows': rows}
        return {'columns': [], 'rows': []}
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

def write_batch_to_target_db(conn, table, columns, data):
    """Executes a batch insert into the target DB."""
    if not data:
        return
    
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        # Generate placeholders: (%s, %s, ...)
        placeholders = "(" + ", ".join(["%s"] * len(columns)) + ")"
        col_names = ", ".join(columns)
        
        # Construct the INSERT query
        # query = f"INSERT INTO {table} ({col_names}) VALUES {placeholders}"
        # Using execute_values for efficiency would be better, but standard executemany is fine for now
        
        from psycopg2.extras import execute_values
        query = f"INSERT INTO {table} ({col_names}) VALUES %s"
        execute_values(cursor, query, data)
        
        print(f"Executed batch insert into {table}: {len(data)} rows")
    except Exception as e:
        print(f"Error executing batch insert into '{table}': {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
