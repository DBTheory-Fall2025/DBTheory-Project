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
        try:
            analysis = similarity_finder.find_similarities(db_connections, status_callback)
        except Exception as e:
            status_callback("error", f"Similarity Finder failed: {str(e)}", None)
            return
        
        # 2. Schema Generator
        try:
            new_schema = schema_generator.generate_schema(analysis, status_callback)
        except Exception as e:
            status_callback("error", f"Schema Generator failed: {str(e)}", None)
            return

        # 3. SQL Generator
        try:
            sql_commands = sql_generator.generate_sql(new_schema, status_callback)
        except Exception as e:
            status_callback("error", f"SQL Generator failed: {str(e)}", None)
            return

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

                # error handler (has built-in retry logic)
                fixed_sql = sql_error_handler.handle_sql_error(stmt, error_msg, status_callback)

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

        # 5. generate the conversion scripts
        try:
            conversion_scripts = conversion_generator.generate_conversion_scripts(analysis, new_schema, sql_commands, status_callback)
        except Exception as e:
            status_callback("error", f"Conversion Generator failed: {str(e)}", None)
            return

        # 6. Logic Checker
        try:
            is_ok = logic_checker.check_logic(analysis, new_schema, sql_commands, conversion_scripts, status_callback)
        except Exception as e:
            status_callback("error", f"Logic Checker failed: {str(e)}", None)
            return
            
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
                status_callback("conversion-error-handler", f"Failed statement {idx}: {error_msg}", "H")

                # AI conversion error handler (has built-in retry logic)
                fixed_stmt = conversion_error_handler.handle_conversion_error(stmt, error_msg, status_callback)

                try:
                    write_to_target_db(new_db_conn, fixed_stmt)
                    conv_success.append(fixed_stmt)
                    status_callback("conversion-error-handler", f"Fixed statement {idx} executed successfully.", "H")
                except Exception as e2:
                    conv_failures.append((stmt, str(e2)))
                    status_callback("conversion-error-handler", f"Retry failed for statement {idx}: {str(e2)}", "H")

            time.sleep(0.5)
        
        status_callback("workflow-complete", "Database combination process completed.", None)

    except Exception as e:
        print(f"An error occurred in the workflow: {e}")
        status_callback("error", str(e), None)
