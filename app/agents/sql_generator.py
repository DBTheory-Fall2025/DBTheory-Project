from ..ai_setup import model

def generate_sql(schema):
    """
    Takes a unified SQL schema and uses an AI model to generate
    the final, executable SQL commands.
    """
    prompt = f"""
Based on the following unified schema, please generate the final, executable SQL `CREATE TABLE` commands.
Ensure that the SQL is valid PostgreSQL.

Schema:
{schema}
"""
    
    sql_commands = model(prompt)
    return sql_commands
