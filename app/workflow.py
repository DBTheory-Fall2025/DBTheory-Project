import time
from .agents import (
    similarity_finder,
    schema_generator,
    sql_generator,
    logic_checker,
)
from .utils.db_util import get_schema, execute_query

def run_workflow(db_connections, new_db_conn, status_callback):
    """
    Orchestrates the agent workflow to combine databases.
    """
    try:
        # 1. Similarity Finder
        status_callback("similarity-finder", "Analyzing database schemas...", "A")
        analysis = similarity_finder.find_similarities(db_connections)
        status_callback("similarity-finder", analysis, "A", is_code=True)
        time.sleep(1)

        # 2. Schema Generator
        status_callback("schema-generator", "Generating a new, unified schema...", "B")
        new_schema = schema_generator.generate_schema(analysis)
        status_callback("schema-generator", new_schema, "B", is_code=True)
        time.sleep(1)

        # 3. SQL Generator
        status_callback("sql-generator", "Generating SQL CREATE TABLE commands...", "D")
        sql_commands = sql_generator.generate_sql(new_schema)
        status_callback("sql-generator", sql_commands, "D", is_code=True)
        time.sleep(1)

        # 4. SQL Executor (Non-agent)
        status_callback("sql-generator", "Executing SQL commands...", "E")
        execute_query(new_db_conn, sql_commands)
        status_callback("sql-generator", "Tables created successfully.", "E")
        time.sleep(1)

        # 5. Logic Checker
        status_callback("logic-checker", "Checking logic and consistency...", "I")
        is_ok = logic_checker.check_logic(analysis, new_schema, sql_commands)
        if is_ok:
            status_callback("logic-checker", "Logic check passed.", "I")
        else:
            status_callback("logic-checker", "Logic check failed. Rerunning...", "I")
        
        status_callback("workflow-complete", "Database combination process completed.", None)

    except Exception as e:
        print(f"An error occurred in the workflow: {e}")
        status_callback("error", str(e), None)
