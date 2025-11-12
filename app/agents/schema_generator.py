from ..ai_setup import model
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU

def generate_schema(analysis):
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
    
    new_schema = model(prompt, agent_name = "schema_generator")
    return new_schema
