import json
import queue
import threading
from flask import Flask, Response, render_template, jsonify, request
import tomli
from .utils.db_util import connect_to_db, create_new_database
from .workflow import run_workflow

app = Flask(__name__)

# In-memory queue for SSE messages
update_queue = queue.Queue()

def get_db_configs():
    with open("config.toml", "rb") as f:
        return tomli.load(f).get("database", {})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-databases', methods=['GET'])
def get_databases():
    db_configs = get_db_configs()
    return jsonify({'success': True, 'databases': list(db_configs.keys())})

def workflow_target(selected_dbs, new_db_name, db_configs):
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
        
        # Create and connect to the new database
        # Assumes a default config can be used for the new DB
        default_config = next(iter(db_configs.values()))
        create_new_database(default_config, new_db_name)
        new_db_conn = connect_to_db(default_config, db_name=new_db_name)

        run_workflow(db_connections, new_db_conn, status_callback)

    except Exception as e:
        status_callback("error", f"Workflow failed: {e}", None)
    finally:
        # Clean up connections
        for conn in db_connections.values():
            conn.close()
        if 'new_db_conn' in locals() and new_db_conn:
            new_db_conn.close()

@app.route('/combine-databases', methods=['POST'])
def combine_databases():
    data = request.json
    selected_dbs = data.get('selected_dbs', [])
    new_db_name = data.get('new_db_name')
    
    if not selected_dbs or not new_db_name:
        return jsonify({'success': False, 'error': 'Missing required parameters'})
    
    db_configs = get_db_configs()
    
    # Start the workflow in a background thread
    thread = threading.Thread(
        target=workflow_target,
        args=(selected_dbs, new_db_name, db_configs)
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
    app.run(debug=True, threaded=True)
