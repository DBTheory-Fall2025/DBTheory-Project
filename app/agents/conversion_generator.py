from ..ai_setup import model
import json
import re

example_json = """{
  "queries": [
    "INSERT INTO ...;",
    "INSERT INTO ...;"
  ]
}"""

def generate_conversion_scripts(analysis, new_schema, sql_commands):
    """
    Generates data conversion scripts based on the analysis and new schema.
    """
    prompt = f"""
You are an expert data engineer. Your task is to generate conversion scripts in the process of combingin two databases. Based on the following analysis and the new unified schema, please generate the SQL `INSERT` statements to migrate the data from the old databases into the new schema.
You can use the `read_sql_data(query)` function to inspect the data in the tables if you need more context.
Pay close attention to data transformations that may be required, such as splitting columns or converting units.
When joining data with keys, the different databases may use different keys. 
In these cases join the keys under one unified key in the new schema (db1Key-db2Key-db3Key etc).
If data exists in one database but not others, ensure it is still included in the new schema with NULLs where appropriate 
(For keys this would be db1Key-NULL-NULL etc).

Please return the result as a valid JSON object with the following structure with no additional notation or comments:   
{example_json}

Analysis:
{analysis}

New Schema:
{new_schema}

create table statements:
{sql_commands}
"""
    
    response = model(prompt, agent_name = "conversion_generator")
    try:
        parsed = json.loads(clean_json_response(response))
        if isinstance(parsed, dict) and "queries" in parsed:
            return parsed["queries"]
        else:
            print("⚠️ Unexpected AI output format, falling back to text parsing.")
            return [q.strip() + ";" for q in response.split(";") if q.strip()]
    except json.JSONDecodeError:
        print("⚠️ Failed to parse AI output as JSON. Falling back to naive splitting.")
        return [q.strip() + ";" for q in response.split(";") if q.strip()]
    
def clean_json_response(response: str):
    # Remove Markdown fences (```json ... ``` or ```; etc.)
    cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", response)
    cleaned = re.sub(r"```;?\s*$", "", cleaned)
    return cleaned.strip()
