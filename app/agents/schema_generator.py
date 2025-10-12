from ..ai_setup import model

def generate_schema(analysis):
    """
    Takes the analysis of database similarities and uses an AI model
    to generate a new, unified schema.
    """
    prompt = f"""
Based on the following analysis of database similarities, please generate a new, unified SQL schema.
The schema should be well-structured and normalized.
Provide only the SQL code for the new schema.

Analysis:
{analysis}
"""
    
    new_schema = model(prompt)
    return new_schema
