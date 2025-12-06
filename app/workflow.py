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
from .utils.db_util import get_schema, write_to_target_db, read_sql_data, write_batch_to_target_db
from .utils.agent_util import send_sql_result

def run_workflow(db_connections, new_db_conn, status_callback):
    """
    Orchestrates the agent workflow to combine databases.
    """
    try:
        # 1. Similarity Finder
        try:
            # Pass None for callback to avoid duplicate messages (agent_util handles streaming)
            analysis = similarity_finder.find_similarities(db_connections, None)
        except Exception as e:
            status_callback("error", f"Similarity Finder failed: {str(e)}", None)
            return
        
        # 2. Schema Generator
        try:
            new_schema = schema_generator.generate_schema(analysis, None)
        except Exception as e:
            status_callback("error", f"Schema Generator failed: {str(e)}", None)
            return

        # 3. SQL Generator
        try:
            sql_commands = sql_generator.generate_sql(new_schema, None)
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
                send_sql_result("sql-executor", "Target DB", stmt, "Success", "E", status_callback)
            except Exception as e:
                error_msg = str(e)
                send_sql_result("sql-error-handler", "Target DB", stmt, f"Failed statement {idx}: {error_msg}", "F", status_callback)

                # error handler (has built-in retry logic)
                fixed_sql = sql_error_handler.handle_sql_error(stmt, error_msg, None)

                # retry fixed sql
                try:
                    write_to_target_db(new_db_conn, fixed_sql)
                    send_sql_result("sql-error-handler", "Target DB", fixed_sql, f"Fixed statement {idx} executed successfully.", "F", status_callback)
                    successful_statements.append(fixed_sql)
                except Exception as e2:
                    send_sql_result("sql-error-handler", "Target DB", fixed_sql, f"Retry failed for statement {idx}: {str(e2)}", "F", status_callback)
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
            conversion_scripts = conversion_generator.generate_conversion_scripts(analysis, new_schema, sql_commands, None)
        except Exception as e:
            status_callback("error", f"Conversion Generator failed: {str(e)}", None)
            return

        # 6. Logic Checker
        try:
            is_ok = logic_checker.check_logic(analysis, new_schema, sql_commands, conversion_scripts, None)
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

        for idx, item in enumerate(conversion_scripts, start=1):
            if isinstance(item, dict):
                # New Transfer Object logic
                target_table = item.get('target_table')
                source_db = item.get('source_db')
                source_query = item.get('source_query')
                target_columns = item.get('target_columns')

                status_callback("conversion-executor", f"Transferring to {target_table}...", "H")
                
                try:
                    if source_db not in db_connections:
                        raise Exception(f"Source DB '{source_db}' not found.")
                    
                    # Fetch data safely
                    source_conn = db_connections[source_db]
                    
                    # Use read_sql_safely to auto-fix query if it fails
                    result_dict = sql_error_handler.read_sql_safely(
                        conn=source_conn,
                        query=source_query,
                        agent_name="conversion-executor",
                        status_callback=status_callback,
                        schema_context=None, # Will auto-fetch if error occurs
                        db_name=source_db,
                        node_id="H"
                    )
                    
                    if not result_dict or not result_dict.get('rows'):
                        status_callback("conversion-executor", f"No data found for {target_table} (Source: {source_db}).", "H")
                        continue

                    data = result_dict['rows']

                    # Insert data
                    write_batch_to_target_db(new_db_conn, target_table, target_columns, data)
                    
                    conv_success.append(item)
                    send_sql_result("conversion-executor", "Target DB", f"Transferred {len(data)} rows to {target_table}", "Success", "H", status_callback)
                
                except Exception as e:
                    error_msg = str(e)
                    conv_failures.append((item, error_msg))
                    send_sql_result("conversion-error-handler", "Target DB", f"Transfer to {target_table}", f"Failed: {error_msg}", "H", status_callback)

            else:
                # Legacy SQL String logic
                stmt = item
                status_callback("conversion-executor", f"Executing statement {idx}/{len(conversion_scripts)}...", "H")
                try:
                    write_to_target_db(new_db_conn, stmt)
                    conv_success.append(stmt)
                    send_sql_result("conversion-executor", "Target DB", stmt, "Success", "H", status_callback)
                except Exception as e:
                    error_msg = str(e)
                    send_sql_result("conversion-error-handler", "Target DB", stmt, f"Failed statement {idx}: {error_msg}", "H", status_callback)

                    # AI conversion error handler (has built-in retry logic)
                    fixed_stmt = conversion_error_handler.handle_conversion_error(stmt, error_msg, None)

                    try:
                        write_to_target_db(new_db_conn, fixed_stmt)
                        conv_success.append(fixed_stmt)
                        send_sql_result("conversion-error-handler", "Target DB", fixed_stmt, f"Fixed statement {idx} executed successfully.", "H", status_callback)
                    except Exception as e2:
                        conv_failures.append((stmt, str(e2)))
                        send_sql_result("conversion-error-handler", "Target DB", fixed_stmt, f"Retry failed for statement {idx}: {str(e2)}", "H", status_callback)

            time.sleep(0.5)
        
        status_callback("workflow-complete", "Database combination process completed.", None)

    except Exception as e:
        print(f"An error occurred in the workflow: {e}")
        status_callback("error", str(e), None)
