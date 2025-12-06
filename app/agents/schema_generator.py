from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message
from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
from ..utils.db_util import write_to_target_db
import json
import re

example_json = """{
  "queries": [
    "CREATE TABLE ...;",
    "CREATE TABLE ...;"
  ]
}"""

def generate_schema(analysis, status_callback=None):
    """
    Takes the analysis of database similarities and uses an AI model
    to generate a new, unified schema and execute the CREATE TABLE commands.
    """
    prompt = f"""
You are an expert data engineer. Your role is to generate SQL statements in the process of combining two databases. You will be given a unified schema.
Based on the following analysis of database similarities, please generate a new, unified SQL schema and then generate valid, executable SQL `CREATE TABLE` commands for a PostgresSQL database.

Please return the result as a valid JSON object with the following structure with no additional notation or comments:   
{example_json}

Analysis:
{analysis}


Return only the JSON object containing the queries, do not return any additional comments, characters, or annotations. 
"""
    
    response = stream_agent_message(
        agent_id="schema-generator",
        node_id="B",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="schema_generator"),
        status_callback=status_callback,
        is_code=True
    )
    
    try:
        parsed = json.loads(clean_json_response(response))
        if isinstance(parsed, dict) and "queries" in parsed:
            queries = parsed["queries"]
        else:
            print("⚠️ Unexpected AI output format, falling back to text parsing.")
            queries = [q.strip() + ";" for q in response.split(";") if q.strip()]
    except json.JSONDecodeError:
        print("⚠️ Failed to parse AI output as JSON. Falling back to naive splitting.")
        queries = [q.strip() + ";" for q in response.split(";") if q.strip()]

    # Execute the CREATE TABLE commands
    for query in queries:
        try:
            write_to_target_db(query)
        except Exception as e:
            print(f"Error executing query: {query}\n{e}")
            # Decide if we want to raise the exception or just log it
            # For now, just log and continue
    
    return queries


def clean_json_response(response: str):
    # Remove Markdown fences (```json ... ``` or ```; etc.)
    cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", response)
    cleaned = re.sub(r"```;?\s*$", "", cleaned)
    return cleaned.strip()
