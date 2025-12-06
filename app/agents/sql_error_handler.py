from ..ai_setup import model_stream, model
from ..utils.agent_util import stream_agent_message, send_sql_result
from ..utils.db_util import read_sql_data_with_headers, get_enhanced_schema
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
import json
import hashlib

def handle_sql_error(sql_commands, error, status_callback=None):
    """
    Handles errors from SQL execution with streaming output.
    """
    print(f"Handle SQL error for query: {sql_commands}")
    print(f"Error: {error}")

    prompt = f"""
        You are an expert SQL engineer. 
        The following SQL statement failed during execution. Analyze the error message 
        and correct the SQL so that it can successfully run in a PostgreSQL database. 

        {PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU}

        --- SQL commands ---
        {sql_commands}

        --- Error message ---
        {error}

        Your task:
        - Fix syntax or reference errors.
        - Ensure table/column names match the schema context.
        - Maintain logical intent (don't change semantics unnecessarily).
        - Return only the corrected SQL, nothing else. Do not return any additional comments or writing.
    """

    fixed_sql = stream_agent_message(
        agent_id="sql-error-handler",
        node_id="F",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="sql_error_handler"),
        status_callback=status_callback,
        is_code=True
    )
    return fixed_sql

def read_sql_safely(conn, query, agent_name, status_callback, schema_context=None, db_name="unknown", node_id="A"):
    """
    Executes a SELECT query safely, attempting to fix it with AI if it fails.
    Returns the result dict {'columns': [], 'rows': []} or None if failed.
    """
    
    # Generate stable message ID for this query execution (for UI updates)
    msg_hash = hashlib.md5(f"{db_name}:{query}".encode()).hexdigest()
    message_id = f"result-{msg_hash}"
    
    # Initial status
    send_sql_result(agent_name, db_name, query, "Executing query...", node_id, status_callback, message_id)
    
    current_query = query
    max_retries = 3
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = read_sql_data_with_headers(conn, current_query)
            # Success! Update UI
            send_sql_result(agent_name, db_name, current_query, result, node_id, status_callback, message_id)
            return result
            
        except Exception as e:
            # Rollback to clear error state
            if hasattr(conn, 'rollback'):
                conn.rollback()
            
            last_error = str(e)
            print(f"Query failed (Attempt {attempt+1}/{max_retries}): {last_error}")
            
            if attempt < max_retries - 1:
                # Update UI to show failure and fixing status
                fail_msg = f"Query failed (Attempt {attempt+1}/{max_retries}): {last_error}\nAttempting to fix..."
                send_sql_result(agent_name, db_name, current_query, fail_msg, node_id, status_callback, message_id)
                
                # Fetch schema if not provided
                if not schema_context:
                    try:
                        print("Fetching schema context for fix...")
                        schema_context = get_enhanced_schema(conn)
                    except Exception as se:
                        print(f"Failed to fetch schema context: {se}")
                        schema_context = "Unavailable"

                # Generate fix
                current_query = _generate_fix(db_name, current_query, last_error, schema_context)
                
                if not current_query:
                    # Fix generation failed
                    break
                
                # Update UI to show new query is being tried
                send_sql_result(agent_name, db_name, current_query, "Retrying with corrected query...", node_id, status_callback, message_id)
            else:
                # Last attempt failed
                pass

    # Final failure
    fail_msg = f"Failed after {max_retries} attempts. Last Error: {last_error}"
    send_sql_result(agent_name, db_name, f"{current_query} (Failed)", fail_msg, node_id, status_callback, message_id)
    return None

def _generate_fix(db_name, query, error, schema_info):
    """
    Internal helper to generate a fixed SQL query using a simple AI call.
    """
    fix_prompt = f"""
The following SQL query failed on database '{db_name}'.
Query: {query}
Error: {error}

Schema for {db_name}:
{schema_info}

Please provide a CORRECTED SQL query that accomplishes the same goal.
Return ONLY the SQL query, nothing else. No markdown.
"""
    try:
        fixed = model(fix_prompt, agent_name="sql-fixer").strip()
        # Cleanup
        if fixed.startswith("```sql"): fixed = fixed[6:]
        if fixed.startswith("```"): fixed = fixed[3:]
        if fixed.endswith("```"): fixed = fixed[:-3]
        return fixed.strip()
    except Exception as e:
        print(f"Fix generation failed: {e}")
        return None
