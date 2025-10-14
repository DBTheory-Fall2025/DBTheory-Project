from ..ai_setup import model

def generate_conversion_scripts(analysis, new_schema):
    """
    Generates data conversion scripts based on the analysis and new schema.
    """
    prompt = f"""
Based on the following analysis and the new unified schema, please generate the SQL `INSERT` statements to migrate the data from the old databases into the new schema.
You can use the `read_sql_data(query)` function to inspect the data in the tables if you need more context.
Pay close attention to data transformations that may be required, such as splitting columns or converting units.

Analysis:
{analysis}

New Schema:
{new_schema}
"""
    
    conversion_scripts = model(prompt)
    return conversion_scripts
