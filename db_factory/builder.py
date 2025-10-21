import json
import os
def main():
    # Load the configuration
    with open('/app/db_factory/config.json', 'r') as f:
        config = json.load(f)

    # Generate the init.sql file
    with open('/app/init.sql', 'w') as f:
        f.write(f"-- this is an auto-generated file by db_factory/builder.py\n\n")
        f.write(f"\c postgres\n")
        for db in config['databases']:
            db_name = db['name']
            user = f"{db_name}_user"
            password = f"{db_name}_password"

            f.write(f"CREATE USER {user} WITH PASSWORD '{password}';\n")
            f.write(f"CREATE DATABASE {db_name};\n")
            f.write(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};\n")
            f.write(f"\\c {db_name}\n\n")

            # Add setup.sql content
            setup_sql_path = os.path.join('/app/data', db_name, db['setup_sql'])
            if os.path.exists(setup_sql_path):
                with open(setup_sql_path, 'r') as setup_f:
                    f.write(setup_f.read())
                f.write('\n\n')

            # Add COPY commands for each CSV
            for csv_file in db['csv_files']:
                table_name = os.path.splitext(csv_file)[0]
                f.write(f"COPY {table_name}\n")
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
