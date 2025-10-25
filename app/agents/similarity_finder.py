from ..ai_setup import model
from ..utils.db_util import get_schema, read_sql_data
import json
read_request = """{
  "read_requests": [
    {"db": "db1", "query": "SELECT * FROM users LIMIT 5"},
    {"db": "db2", "query": "SELECT * FROM members LIMIT 5"}
  ]
}"""

analysis_json = """{
  "analysis": "Detailed comparison and merge plan here."
}"""

def find_similarities(db_connections):
    """
    Analyzes the schemas of the given databases and uses an AI model
    to find similarities between them.
    """
    schemas = {}
    for db_name, conn in db_connections.items():
        schema = get_schema(conn)
        print(f"[DEBUG] Schema returned for {db_name}: {schema}", flush=True)
        schemas[db_name] = get_schema(conn)

    print("\n=== DATABASE SCHEMAS ===")
    for db_name, schema_info in schemas.items():
        print(f"\nDatabase: {db_name}")
        for table_name, columns in schema_info.items():
            print(f"  Table: {table_name}")
            for col_name, col_type in columns.items():
                print(f"    - {col_name} ({col_type})")
    print("=========================\n", flush=True)

    # Format the schemas into a prompt for the AI
    schema_text = ""
    for db_name, schema_info in schemas.items():
        schema_text += f"Database: {db_name}\n"
        for table_name, columns in schema_info.items():
            schema_text += f"  Table: {table_name}\n"
            for col_name, col_type in columns.items():
                schema_text += f"    - {col_name} ({col_type})\n"
        schema_text += "\n"

    prompt = f"""
You are an advanced data engineeri tasked with merging two databses. Please analyze these schemas and identify columns and tables that are similar and could be merged.
You can use the `read_sql_data(query)` function to inspect the data in the tables to get a better understanding of the contents.
For example, you can run `read_sql_data("SELECT * FROM users LIMIT 5")` to see a few rows from the users table.
Provide a detailed analysis of the similarities and a plan for merging the data.
here are there schemas:
{schema_text}
If you want to see actual sample data, you may request it by responding ONLY with
a JSON object like this:

{read_request}

If you have enough information already, respond with a JSON object like this:

{analysis_json}
"""

    # Get the AI's analysis
    ai_response = model(prompt)
    analysis = ai_response

    if isinstance(ai_response, str) and '"read_requests"' in ai_response:
        errors_occurred = False
        data_samples = {}
        try:
            request_obj = json.loads(ai_response.strip())
        except json.JSONDecodeError as e:
            errors_occurred = True
            request_obj = {"read_requests": []}
        
        

        for req in request_obj.get("read_requests", []):
            db_name = req.get("db")
            query = req.get("query")

            if not db_name or not query:
                continue
            if db_name not in db_connections:
                data_samples[f"{db_name}:{query}"] = "Error: unknown database name"
                errors_occurred = True
                continue

            try:
                result = read_sql_data(db_connections[db_name], query)
                data_samples[f"{db_name}:{query}"] = result
            except Exception as e:
                data_samples[f"{db_name}:{query}"] = f"Error executing query: {e}"
                errors_occurred = True

        # Build the follow-up prompt
        if errors_occurred:
            re_prompt = f"""
Some of your requested queries could not be executed due to database limitations or errors.

Please proceed with your similarity analysis based on the available schema and partial data.
Return your final analysis and merge plan as JSON in the format:

{analysis_json}
"""
        else:
            re_prompt = f"""
Here are the results of your requested queries:

{json.dumps(data_samples, indent=2)}

Now re-analyze the schemas using this data context,
and provide your final similarity analysis and merge plan as JSON:

{analysis_json}
"""

        analysis = model(re_prompt)

    # TODO: Give the ai the result of it's read_sql_data(query) & have it re-analyze if it wishes
    return analysis
