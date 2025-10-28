from .constants.prompt_constants import PLEASE_ONLY_CODE_PLEASE_I_BEG_YOU
from ..ai_setup import model
import json
import re

example_json = """{
  "queries": [
    "CREATE TABLE ...;",
    "CREATE TABLE ...;"
  ]
}"""

def generate_sql(schema):
  """
  Takes a unified SQL schema and uses an AI model to generate
  the final, executable SQL commands.
  """
  prompt = f"""
You are an expert data engineer. Your role is to generate SQL statements in the process of combining two databases. You will be given a unified schema.
Based on the following unified schema, please generate valid, executable SQL `CREATE TABLE` commands for a PostgresSQL database.

Please return the result as a valid JSON object with the following structure with no additional notation or comments:   
{example_json}

Schema:
{schema}


Return only the JSON object containing the queries, do not return any additional comments, characters, or annotations. 
"""
    
  response = model(prompt, agent_name = "sql_generator")
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