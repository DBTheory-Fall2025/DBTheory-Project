from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
import json

def handle_conversion_error(script, error, status_callback=None):
    """
    Handles errors from conversion scripts with streaming output.
    """
    print(f"Handle SQL error for query: {script}")
    print(f"Error: {error}")

    prompt = f"""
        You are an expert SQL engineer. 
        The following SQL statement failed during execution. Analyze the error message 
        and correct the SQL so that it can successfully run in a PostgreSQL database. 

        {PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU}

        --- SQL commands ---
        {script}

        --- Error message ---
        {error}

        Your task:
        - Fix syntax or reference errors.
        - Ensure table/column names match the schema context.
        - Maintain logical intent (don't change semantics unnecessarily).
        - Return only the corrected SQL, nothing else. Do not return any additional comments or writing.
    """

    fixed_sql = stream_agent_message(
        agent_id="conversion-error-handler",
        node_id="H",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="conversion_error_handler"),
        status_callback=status_callback,
        is_code=True
    )
    return fixed_sql
