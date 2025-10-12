from ..ai_setup import model
from ..utils.db_util import get_schema

def find_similarities(db_connections):
    """
    Analyzes the schemas of the given databases and uses an AI model
    to find similarities between them.
    """
    schemas = {}
    for db_name, conn in db_connections.items():
        schemas[db_name] = get_schema(conn)

    # Format the schemas into a prompt for the AI
    prompt = "Here are the schemas of the databases to be combined:\n\n"
    for db_name, schema_info in schemas.items():
        prompt += f"Database: {db_name}\n"
        for table_name, columns in schema_info.items():
            prompt += f"  Table: {table_name}\n"
            for col_name, col_type in columns.items():
                prompt += f"    - {col_name} ({col_type})\n"
        prompt += "\n"

    prompt += "Please analyze these schemas and identify columns and tables that are similar and could be merged. Provide a detailed analysis."

    # Get the AI's analysis
    analysis = model(prompt)
    return analysis
