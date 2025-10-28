import json
import os
import pandas as pd
from typing import Dict, List, Tuple

def detect_csv_columns(csv_path: str) -> Tuple[List[str], Dict[str, str]]:
    """Detect column names and data types from a CSV file."""
    try:
        # Read the first few rows to detect types
        df = pd.read_csv(csv_path, nrows=100)
        
        # Get column names
        columns = df.columns.tolist()
        
        # Detect data types
        data_types = {}
        for column in columns:
            # Convert pandas types to PostgreSQL types
            dtype = df[column].dtype
            if dtype == 'object':
                # String type
                data_types[column] = 'VARCHAR(255)'
            elif dtype == 'int64':
                data_types[column] = 'INTEGER'
            elif dtype == 'float64':
                data_types[column] = 'DECIMAL'
            elif dtype == 'datetime64[ns]':
                data_types[column] = 'TIMESTAMP'
            else:
                # Default to VARCHAR if unsure
                data_types[column] = 'VARCHAR(255)'
                
        return columns, data_types
    except Exception as e:
        print(f"Error reading CSV file {csv_path}: {str(e)}")
        return [], {}

def main():
    # Load the configuration
    with open('/app/db_factory/config.json', 'r') as f:
        config = json.load(f)
    
    # Generate the init.sql file
    with open('/app/init.sql', 'w') as f:
        f.write(f"-- this is an auto-generated file by db_factory/builder.py\n\n")
        
        # Create databases and users in postgres database
        for db in config['databases']:
            db_name = db['name']
            user = f"{db_name}_user"
            password = f"{db_name}_password"
            
            f.write(f"CREATE USER {user} WITH PASSWORD '{password}';\n")
            f.write(f"CREATE DATABASE {db_name};\n")
            f.write(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};\n\n")
            
            # Initialize the database
            f.write(f"SET search_path TO {db_name};\n\n")
            
            # Process each CSV file
            for csv_file in db['csv_files']:
                table_name = os.path.splitext(csv_file)[0]
                csv_path = os.path.join('/app/data', db_name, csv_file)
                
                # Detect columns and types
                columns, data_types = detect_csv_columns(csv_path)
                
                # Create table
                f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
                for column in columns:
                    f.write(f"    {column} {data_types[column]},\n")
                f.write("    PRIMARY KEY (" + ", ".join(columns) + ")\n")
                f.write(");\n\n")
                
                # Copy data
                f.write(f"COPY {table_name} ({', '.join(columns)})\n")
                f.write(f"FROM '/data/{db_name}/{csv_file}'\n")
                f.write("DELIMITER ','\n")
                f.write("CSV HEADER;\n\n")

    # Prepare the database configurations
    db_configs = {}
    for db in config['databases']:
        db_name = db['name']
        db_configs[db_name] = {
            "host": "postgres",
            "port": 5432,
            "user": f"{db_name}_user",
            "password": f"{db_name}_password",
            "dbname": db_name
        }

    if 'external_databases' in config:
        for db in config['external_databases']:
            db_name = db['name']
            db_configs[db_name] = {
                "host": db["host"],
                "port": db["port"],
                "user": db["user"],
                "password": db["password"],
                "dbname": db["dbname"]
            }

    # Write the database configurations to a JSON file
    with open('/config/db_config.json', 'w') as f:
        json.dump(db_configs, f, indent=2)
    print("Successfully wrote database configurations to /config/db_config.json")

if __name__ == '__main__':
    main()