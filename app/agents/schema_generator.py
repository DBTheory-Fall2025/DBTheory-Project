from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU

def generate_schema(analysis, status_callback=None):
    """
    Takes the analysis of database similarities and uses an AI model
    to generate a new, unified schema.
    """
    prompt = f"""
Based on the following analysis of database similarities, please generate a new, unified SQL schema.
The schema should be well-structured and normalized.
{PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU}

Analysis:
{analysis}
"""
    
    new_schema = stream_agent_message(
        agent_id="schema-generator",
        node_id="B",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="schema_generator"),
        status_callback=status_callback,
        is_code=True
    )
    return new_schema
