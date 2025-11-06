import json
import os
import queue
import threading
from flask import Flask, Response, render_template, jsonify, request
from .utils.db_util import connect_to_db
from .utils.agent_util import set_update_queue
from .workflow import run_workflow

app = Flask(__name__)

# In-memory storage for database configurations
db_configs_in_memory = {}

# In-memory queue for SSE messages
update_queue = queue.Queue()

# Initialize the agent utility with the update queue
set_update_queue(update_queue)

def load_db_configs():
    global db_configs_in_memory
    config_path = "/config/db_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            db_configs_in_memory = json.load(f)
        print("Database configurations loaded successfully.")
    else:
        print("Config file not found, starting with empty DB configs.")

load_db_configs()

def get_db_configs():
    return db_configs_in_memory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-databases', methods=['GET'])
def get_databases():
    db_configs = get_db_configs()
    return jsonify({'success': True, 'databases': list(db_configs.keys())})

def workflow_target(selected_dbs, db_configs, target_db_config):
    """Target function for the background thread."""
    
    def status_callback(agent_id, message, node_id, is_code=False):
        update = {
            "agentId": agent_id,
            "message": message,
            "nodeId": node_id,
            "isCode": is_code,
        }
        update_queue.put(json.dumps(update))

    try:
        # Establish connections to selected databases
        db_connections = {
            name: connect_to_db(params)
            for name, params in db_configs.items()
            if name in selected_dbs
        }
        
        # Connect to the target database
        target_db_conn = connect_to_db(target_db_config)

        # Check for connection failures
        has_target_failure = target_db_config is None
        failed_source_dbs = {name: conn for name, conn in db_connections.items() if conn is None}
        has_source_failures = len(failed_source_dbs) > 0
        if has_target_failure or has_source_failures:
            error_messages = []
    
            if has_target_failure:
                error_messages.append("Target database")
                
            if has_source_failures:
                error_messages.extend(f"Source database '{name}'" for name in failed_source_dbs.keys())
            
            raise Exception(
                f"Could not connect to {', '.join(error_messages)}. "
                "Check your database configurations and verify the databases are accessible."
            )

        run_workflow(db_connections, target_db_conn, status_callback)

    except Exception as e:
        status_callback("error", f"Workflow failed: {e}", None)
    finally:
        # Clean up connections
        for conn in db_connections.values():
            if conn == None:
                continue # connection was never established
            conn.close()
        if 'target_db_conn' in locals() and target_db_conn:
            target_db_conn.close()

@app.route('/combine-databases', methods=['POST'])
def combine_databases():
    data = request.json
    selected_dbs = data.get('selected_dbs', [])
    
    if not selected_dbs:
        return jsonify({'success': False, 'error': 'No databases selected'})
    
    db_configs = get_db_configs()
    
    # Load target DB config from environment variables
    target_db_config = {
        "host": "dbTarget",
        "port": 5432,
        "user": os.getenv("DBTARGET_USER"),
        "password": os.getenv("DBTARGET_PASSWORD"),
        "dbname": os.getenv("DBTARGET_NAME"),
    }

    # Start the workflow in a background thread
    thread = threading.Thread(
        target=workflow_target,
        args=(selected_dbs, db_configs, target_db_config)
    )
    thread.start()
    
    return jsonify({'success': True, 'message': 'Workflow started.'})

@app.route('/status')
def status():
    def event_stream():
        while True:
            try:
                # Wait for a message and send it
                message = update_queue.get(timeout=10)
                yield f"data: {message}\n\n"
            except queue.Empty:
                # Send a comment to keep the connection alive
                yield ": keep-alive\n\n"
    
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/get-tables')
def get_tables():
    try:
        target_db_config = {
            "host": "dbTarget",
            "port": 5432,
            "user": os.getenv("DBTARGET_USER"),
            "password": os.getenv("DBTARGET_PASSWORD"),
            "dbname": os.getenv("DBTARGET_NAME"),
        }
        
        conn = connect_to_db(target_db_config)
        cur = conn.cursor()
        
        # Query to get all tables in the public schema
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True, 'tables': tables})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-table-data')
def get_table_data():
    table = request.args.get('table')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 25))
    offset = (page - 1) * size
    
    try:
        target_db_config = {
            "host": "dbTarget",
            "port": 5432,
            "user": os.getenv("DBTARGET_USER"),
            "password": os.getenv("DBTARGET_PASSWORD"),
            "dbname": os.getenv("DBTARGET_NAME"),
        }
        
        conn = connect_to_db(target_db_config)
        cur = conn.cursor()
        
        # Get column names
        cur.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = %s 
            ORDER BY ordinal_position
        """, (table,))
        columns = [row[0] for row in cur.fetchall()]
        
        # Get paginated data
        cur.execute(f"SELECT * FROM {table} LIMIT %s OFFSET %s", (size, offset))
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'columns': columns,
            'rows': rows
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/search-table')
def search_table():
    table = request.args.get('table')
    search = request.args.get('search', '').strip()
    
    try:
        target_db_config = {
            "host": "dbTarget",
            "port": 5432,
            "user": os.getenv("DBTARGET_USER"),
            "password": os.getenv("DBTARGET_PASSWORD"),
            "dbname": os.getenv("DBTARGET_NAME"),
        }
        
        conn = connect_to_db(target_db_config)
        cur = conn.cursor()
        
        # Get column names
        cur.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = %s 
            ORDER BY ordinal_position
        """, (table,))
        columns = [row[0] for row in cur.fetchall()]
        
        if search:
            # Build a query that searches across all columns
            search_conditions = " OR ".join([
                f"CAST({col} AS TEXT) ILIKE %s" 
                for col in columns
            ])
            query = f"""
                SELECT * FROM {table}
                WHERE {search_conditions}
                LIMIT 100
            """
            # Create parameters array with search term for each column
            params = [f'%{search}%'] * len(columns)
            cur.execute(query, params)
        else:
            # If no search term, return first page
            cur.execute(f"SELECT * FROM {table} LIMIT 25")
        
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'columns': columns,
            'rows': rows
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/execute-sql', methods=['POST'])
def execute_sql():
    query = request.json.get('query', '').strip()
    
    if not query:
        return jsonify({'success': False, 'error': 'No query provided'})
    
    try:
        target_db_config = {
            "host": "dbTarget",
            "port": 5432,
            "user": os.getenv("DBTARGET_USER"),
            "password": os.getenv("DBTARGET_PASSWORD"),
            "dbname": os.getenv("DBTARGET_NAME"),
        }
        
        conn = connect_to_db(target_db_config)
        cur = conn.cursor()
        
        try:
            cur.execute(query)
            conn.commit()  # Commit for all queries to ensure changes are saved
            
            if query.lower().strip().startswith(('select', 'show', 'with')):
                if cur.description:  # Check if the query returned any columns
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    result = {
                        'success': True,
                        'columns': columns,
                        'rows': rows
                    }
                else:
                    # Query was a SELECT but returned no results
                    result = {
                        'success': True,
                        'message': 'Query executed successfully, but returned no results.',
                        'columns': [],
                        'rows': []
                    }
            else:
                # Non-SELECT queries
                result = {
                    'success': True,
                    'message': f'Query executed successfully. Rows affected: {cur.rowcount}'
                }
            
            cur.close()
            conn.close()
            
            return jsonify(result)
            
        except Exception as e:
            if conn:
                conn.rollback()  # Rollback on error
                cur.close()
                conn.close()
            return jsonify({
                'success': False,
                'error': f'Database error: {str(e)}'  # Only show 'Database error' for actual DB errors
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Connection error: {str(e)}'  # Connection errors handled separately
        })

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
