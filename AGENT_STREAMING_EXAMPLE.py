"""
EXAMPLE: How to convert an agent to use streaming

This shows the before/after of converting conversion_error_handler.py
"""

# ============================================================================
# BEFORE: Non-streaming version (still works, but not as visually pleasing)
# ============================================================================

"""
from ..ai_setup import model
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
import json

def handle_conversion_error(script, error):
    print(f"Handle SQL error for query: {script}")
    print(f"Error: {error}")

    prompt = f'''
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
    '''

    fixed_sql = model(prompt, agent_name="conversion_error_handler")
    return fixed_sql
"""

# ============================================================================
# AFTER: Streaming version (real-time token-by-token display)
# ============================================================================

from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
import json


def handle_conversion_error(script, error, status_callback=None):
    """
    Handles errors from conversion scripts with streaming output.
    
    Args:
        script: The SQL script that failed
        error: The error message from the database
        status_callback: Optional callback for status updates (backward compatibility)
    
    Returns:
        The corrected SQL script
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

    # Get streaming response from the API
    stream_generator = model_stream(prompt, agent_name="conversion_error_handler")
    
    # Stream the response to the frontend in real-time
    fixed_sql = stream_agent_message(
        agent_id="conversion-error-handler",  # Matches the tab ID in index.html
        node_id="H",  # The workflow diagram node
        message_generator=stream_generator,
        status_callback=status_callback,
        is_code=True  # Format as code block
    )
    
    return fixed_sql


# ============================================================================
# ADVANCED: Using thinking panes for detailed error analysis
# ============================================================================

"""
from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message, stream_thinking_pane
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU


def handle_conversion_error_with_thinking(script, error, status_callback=None):
    '''
    Handles errors with visible thinking process.
    User can see the AI's analysis before the solution.
    '''
    
    # First, let the AI think about the problem
    thinking_prompt = f'''
        Analyze this SQL error without fixing it yet.
        What is the root cause? What went wrong?
        
        --- SQL commands ---
        {script}

        --- Error message ---
        {error}
    '''
    
    thinking_stream = model_stream(thinking_prompt, agent_name="conversion_error_handler")
    thinking_text = stream_thinking_pane(
        agent_id="conversion-error-handler",
        thinking_generator=thinking_stream,
        status_callback=status_callback
    )
    
    # Now generate the fix
    fix_prompt = f'''
        Based on your analysis of the error, provide the corrected SQL.
        
        {PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU}
        
        --- Original Error ---
        {error}
        
        Return only the corrected SQL, nothing else.
    '''
    
    fix_stream = model_stream(fix_prompt, agent_name="conversion_error_handler")
    fixed_sql = stream_agent_message(
        agent_id="conversion-error-handler",
        node_id="H",
        message_generator=fix_stream,
        status_callback=status_callback,
        is_code=True
    )
    
    return fixed_sql
"""

# ============================================================================
# KEY CHANGES:
# ============================================================================

"""
1. Import Changes:
   - Import: model_stream instead of model
   - Import: stream_agent_message and optionally stream_thinking_pane
   
2. Function Changes:
   - Call model_stream(prompt) to get a generator
   - Pass generator to stream_agent_message()
   - The function handles the SSE streaming automatically
   - Return the accumulated result
   
3. Parameters:
   - Pass agent_id matching your tab ID (e.g., "conversion-error-handler")
   - Pass node_id matching your workflow diagram (e.g., "H")
   - Set is_code=True for SQL, JSON, etc.
   
4. Optional Status Callback:
   - Still supported for backward compatibility
   - Can be omitted if not needed
   
5. Advanced Option:
   - Use stream_thinking_pane() for intermediate reasoning
   - Thinking is displayed in collapsed pane
   - User can expand to see AI's thought process
"""
