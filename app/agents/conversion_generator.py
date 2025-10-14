from ..ai_setup import model

def generate_conversion_scripts(analysis, new_schema):
    """
    Generates data conversion scripts based on the analysis and new schema.
    """
    prompt = f"""
Based on the following analysis and the new unified schema, please generate the SQL `INSERT` statements to migrate the data from the old databases into the new schema.
You can use the `read_sql_data(query)` function to inspect the data in the tables if you need more context.
Pay close attention to data transformations that may be required, such as splitting columns or converting units.
When joining data with keys, the different databases may use different keys. 
In these cases join the keys under one unified key in the new schema (db1Key-db2Key-db3Key etc).
If data exists in one database but not others, ensure it is still included in the new schema with NULLs where appropriate 
(For keys this would be db1Key-NULL-NULL etc).

Analysis:
{analysis}

New Schema:
{new_schema}
"""
    
    conversion_scripts = model(prompt)
    return conversion_scripts
