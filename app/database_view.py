from flask import jsonify, request, Blueprint
import os
from .utils.db_util import connect_to_db

database_view = Blueprint('database_view', __name__)

def register_database_view_routes(app):
    app.register_blueprint(database_view)
    @database_view.route('/get-tables')
    def get_tables():
        try:
            target_db_config = get_target_db_config()
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

    @database_view.route('/get-table-data')
    def get_table_data():
        table = request.args.get('table')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 25))
        offset = (page - 1) * size
        
        try:
            target_db_config = get_target_db_config()
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

    @database_view.route('/search-table')
    def search_table():
        table = request.args.get('table')
        search = request.args.get('search', '').strip()
        
        try:
            target_db_config = get_target_db_config()
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

    @database_view.route('/execute-sql', methods=['POST'])
    def execute_sql():
        query = request.json.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'})
        
        try:
            target_db_config = get_target_db_config()
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

def get_target_db_config():
    return {
        "host": "dbTarget",
        "port": 5432,
        "user": os.getenv("DBTARGET_USER"),
        "password": os.getenv("DBTARGET_PASSWORD"),
        "dbname": os.getenv("DBTARGET_NAME"),
    }