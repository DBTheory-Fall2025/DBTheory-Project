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
            dtype = str(df[column].dtype)
            if 'object' in dtype:
                data_types[column] = 'VARCHAR(255)'
            elif 'int' in dtype:
                data_types[column] = 'INTEGER'
            elif 'float' in dtype:
                data_types[column] = 'DECIMAL'
            elif 'datetime' in dtype:
                data_types[column] = 'TIMESTAMP'
            else:
                # Default to VARCHAR if unsure
                data_types[column] = 'VARCHAR(255)'
                
        return columns, data_types
    except Exception as e:
        print(f"Error reading CSV file {csv_path}: {str(e)}")
        return [], {}

def sanitize(name: str) -> str:
    """Sanitize database, table, and column names."""
    return name.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace('/', '').replace('.', '')

def main():
    seed_data_dir = '/app/seed-data'
    init_sql_path = '/app/init.sql'
    db_configs_path = '/config/db_config.json'
    
    db_configs = {}

    with open(init_sql_path, 'w') as f:
        f.write("-- this is an auto-generated file by db_factory/builder.py\n\n")

        # Iterate over directories in seed-data
        for dir_name in os.listdir(seed_data_dir):
            dir_path = os.path.join(seed_data_dir, dir_name)
            if not os.path.isdir(dir_path):
                continue

            # Find the SQL file
            sql_file = None
            for file_name in os.listdir(dir_path):
                if file_name.endswith('.sql'):
                    sql_file = file_name
                    break
            
            if not sql_file:
                print(f"Skipping directory '{dir_name}': No .sql file found. Please add one to include this dataset.")
                continue

            db_name = sanitize(dir_name.lower())
            user = f"{db_name}_user"
            password = f"{db_name}_password"

            # Create database and user
            f.write(f"CREATE USER {user} WITH PASSWORD '{password}';\n")
            f.write(f"CREATE DATABASE {db_name};\n")
            f.write(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};\n\n")
            
            # Connect to the new database to run further commands
            f.write(f"\\c {db_name}\n\n")

            # First, execute the user-provided SQL file to create the schema
            with open(os.path.join(dir_path, sql_file), 'r') as sql_f:
                f.write(f"-- Contents from {sql_file} to create schema\n")
                f.write(sql_f.read())
                f.write("\n\n")

            # Second, process CSV files to populate the tables
            csv_files = [fname for fname in os.listdir(dir_path) if fname.lower().endswith(('.csv', '.cvs'))]
            for csv_file in csv_files:
                table_name = sanitize(os.path.splitext(csv_file)[0])
                csv_path = os.path.join(dir_path, csv_file)
                
                columns, _ = detect_csv_columns(csv_path)
                
                if not columns:
                    print(f"Could not detect columns for {csv_path}, skipping data copy.")
                    continue
                
                sanitized_columns = [sanitize(c) for c in columns]
                
                # Copy data into the existing table
                f.write(f"-- Populating {table_name} from {csv_file}\n")
                column_list_str = ', '.join([f'"{c}"' for c in sanitized_columns])
                f.write(f'COPY "{table_name}" ({column_list_str})\n')
                f.write(f"FROM '/data/{dir_name}/{csv_file}'\n")
                f.write("DELIMITER ','\n")
                f.write("CSV HEADER;\n\n")

            # Prepare the database configuration
            db_configs[db_name] = {
                "host": "postgres",
                "port": 5432,
                "user": user,
                "password": password,
                "dbname": db_name
            }

    # Write the database configurations to a JSON file
    with open(db_configs_path, 'w') as f:
        json.dump(db_configs, f, indent=2)
    print(f"Successfully wrote database configurations to {db_configs_path}")

if __name__ == '__main__':
    main()
