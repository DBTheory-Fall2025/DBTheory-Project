from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
import json

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
