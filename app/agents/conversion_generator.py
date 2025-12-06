from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message
import json
import re

example_json = """{
  "transfers": [
    {
      "source_db": "SourceDBName",
      "source_query": "SELECT colA, colB FROM source_table",
      "target_table": "TargetTableName",
      "target_columns": ["colX", "colY"]
    }
  ]
}"""

def generate_conversion_scripts(analysis, new_schema, sql_commands, status_callback=None):
    """
    Generates data conversion scripts based on the analysis and new schema.
    """
    prompt = f"""
You are an expert data engineer. Your task is to generate a Data Transfer Plan to combine two databases. 
Based on the following analysis and the new unified schema, please generate a plan to migrate the data from the old databases into the new schema.

Since the databases are on separate connections, you CANNOT use `INSERT INTO target SELECT FROM source`.
Instead, you must provide a list of transfer objects where each object defines:
1. `source_db`: The name of the source database (as seen in the analysis).
2. `source_query`: A SQL `SELECT` query to fetch the raw data from the source table.
3. `target_table`: The name of the table in the new schema to insert into.
4. `target_columns`: The list of column names in the target table that match the columns returned by `source_query` (in order).

Pay close attention to data transformations that may be required in the `source_query` (e.g. casting types, formatting strings).
When joining data with keys, the different databases may use different keys. 
In these cases join the keys under one unified key in the new schema (db1Key-db2Key-db3Key etc).
If data exists in one database but not others, ensure it is still included in the new schema with NULLs where appropriate.

Please return the result as a valid JSON object with the following structure with no additional notation or comments:   
{example_json}

Analysis:
{analysis}

New Schema:
{new_schema}

create table statements:
{sql_commands}
"""
    
    response = stream_agent_message(
        agent_id="conversion-generator",
        node_id="C",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="conversion_generator"),
        status_callback=status_callback,
        is_code=True
    )
    try:
        parsed = json.loads(clean_json_response(response))
        if isinstance(parsed, dict) and "transfers" in parsed:
            return parsed["transfers"]
        elif isinstance(parsed, dict) and "queries" in parsed:
            # Fallback for legacy format or if AI messed up
            return parsed["queries"]
        else:
            print("⚠️ Unexpected AI output format, falling back to text parsing.")
            # If it's just SQL text, wrap it in a pseudo-object or fail
            return [] 
    except json.JSONDecodeError:
        print("⚠️ Failed to parse AI output as JSON.")
        return []
    
def clean_json_response(response: str):
    # Remove Markdown fences (```json ... ``` or ```; etc.)
    cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", response)
    cleaned = re.sub(r"```;?\s*$", "", cleaned)
    return cleaned.strip()
