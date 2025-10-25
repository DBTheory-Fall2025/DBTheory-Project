import time
from .agents import (
    similarity_finder,
    schema_generator,
    sql_generator,
    logic_checker,
    sql_error_handler,
    conversion_generator,
    conversion_error_handler,
)
from .utils.db_util import get_schema, write_to_target_db

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
        status_callback("sql-exeuter", "Executing SQL commands...", "E")
        
        successful_statements = []
        failed_statements = []

        for idx, stmt in enumerate(sql_commands, start=1):
            status_callback("sql-executor", f"Executing statement {idx}/{len(sql_commands)}...", "E")
            try:
                write_to_target_db(new_db_conn, stmt)
                successful_statements.append(stmt)
                status_callback("sql-executor", f"Success:\n{stmt}", "E", is_code=True)
            except Exception as e:
                error_msg = str(e)
                status_callback("sql-error-handler", f"Failed statement {idx}: {error_msg}", "F")

                # error handler
                fixed_sql = sql_error_handler.handle_sql_error(stmt, error_msg)
                status_callback("sql-error-handler", f"AI fixed statement {idx}:\n{fixed_sql}", "F", is_code=True)

                # retry fixed sql
                try:
                    write_to_target_db(new_db_conn, fixed_sql)
                    status_callback("sql-error-handler", f"Fixed statement {idx} executed successfully.", "F")
                    successful_statements.append(fixed_sql)
                except Exception as e2:
                    status_callback("sql-error-handler", f"Retry failed for statement {idx}: {str(e2)}", "F")
                    failed_statements.append((stmt, str(e2)))

            time.sleep(0.5)

        # Report summary
        status_callback(
            "sql-summary",
            f"SQL Execution Summary:\n"
            f"Successful statements: {len(successful_statements)}\n"
            f"Failed statements: {len(failed_statements)}",
            "E"
        )

        if failed_statements:
            status_callback("sql-summary", f"⚠️ Some statements could not be fixed:\n{failed_statements}", "E")

        time.sleep(1)

        # 5. generate the conversion scripts
        status_callback("conversion-generator", "Generating SQL INSERT INTO commands...", "G")
        conversion_scripts = conversion_generator.generate_conversion_scripts(analysis,new_schema,sql_commands)
        status_callback("conversion-generator", conversion_scripts, "G", is_code=True)
        time.sleep(1)

        # 6. Logic Checker
        status_callback("logic-checker", "Checking logic and consistency...", "I")
        is_ok = logic_checker.check_logic(analysis, new_schema, sql_commands, conversion_scripts)
        if is_ok:
            status_callback("logic-checker", "Logic check passed.", "I")
        else:
            status_callback("logic-checker", "Logic check failed. Rerunning...", "I")
        
        #7. execute the conversion scripts and handle errors
        status_callback("conversion-executor", "Executing conversion scripts...", "H")
        conv_success = []
        conv_failures = []

        for idx, stmt in enumerate(conversion_scripts, start=1):
            status_callback("conversion-executor", f"Executing statement {idx}/{len(conversion_scripts)}...", "H")
            try:
                write_to_target_db(new_db_conn, stmt)
                conv_success.append(stmt)
                status_callback("conversion-executor", f"Success:\n{stmt}", "H", is_code=True)
            except Exception as e:
                error_msg = str(e)
                status_callback("conversion-error-handler", f"Failed statement {idx}: {error_msg}", "I")

                # AI conversion error handler
                fixed_stmt = conversion_error_handler.handle_conversion_error(stmt, error_msg)
                status_callback("conversion-error-handler", f"AI fixed statement {idx}:\n{fixed_stmt}", "I", is_code=True)

                try:
                    write_to_target_db(new_db_conn, fixed_stmt)
                    conv_success.append(fixed_stmt)
                    status_callback("conversion-error-handler", f"Fixed statement {idx} executed successfully.", "I")
                except Exception as e2:
                    conv_failures.append((stmt, str(e2)))
                    status_callback("conversion-error-handler", f"Retry failed for statement {idx}: {str(e2)}", "I")

            time.sleep(0.5)
        
        status_callback("workflow-complete", "Database combination process completed.", None)

    except Exception as e:
        print(f"An error occurred in the workflow: {e}")
        status_callback("error", str(e), None)
