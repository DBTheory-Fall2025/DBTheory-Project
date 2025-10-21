import json
import os
import queue
import threading
from flask import Flask, Response, render_template, jsonify, request
from .utils.db_util import connect_to_db
from .workflow import run_workflow

app = Flask(__name__)

# In-memory storage for database configurations
db_configs_in_memory = {}

# In-memory queue for SSE messages
update_queue = queue.Queue()

def load_db_configs():
    global db_configs_in_memory
    config_path = "/config/db_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            db_configs_in_memory = json.load(f)
        print("Database configurations loaded successfully.")
    else:
        print("Config file not found, starting with empty DB configs.")

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
        if not target_db_conn:
            raise Exception("Could not connect to the target database.")

        run_workflow(db_connections, target_db_conn, status_callback)

    except Exception as e:
        status_callback("error", f"Workflow failed: {e}", None)
    finally:
        # Clean up connections
        for conn in db_connections.values():
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

if __name__ == '__main__':
    load_db_configs()
    app.run(debug=True, threaded=True)
