from flask import Flask, render_template, jsonify, request
import tomli
from utils.db_util import connect_to_db, create_new_database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-databases', methods=['GET'])
def get_databases():
    connections = {}
    try:
        with open("config.toml", "rb") as f:
            config = tomli.load(f)
        db_configs = config.get("database", {})
        
        for db_name, db_params in db_configs.items():
            conn = connect_to_db(db_params)
            if conn:
                connections[db_name] = conn
        
        return jsonify({
            'success': True,
            'databases': list(connections.keys())
        })
    finally:
        for conn in connections.values():
            conn.close()

@app.route('/combine-databases', methods=['POST'])
def combine_databases():
    data = request.json
    selected_dbs = data.get('selected_dbs', [])
    new_db_name = data.get('new_db_name')
    
    if not selected_dbs or not new_db_name:
        return jsonify({
            'success': False,
            'error': 'Missing required parameters'
        })
    
    try:
        create_new_database(new_db_name)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
