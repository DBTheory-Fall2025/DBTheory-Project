import tomli
from utils.db_util import connect_to_db, create_new_database

def combine_databases(selected_dbs, new_db_name):
    """
    TODO: Implement the AI workflow to combine the databases into one.
    """
    print(f"//TODO: Combine databases {', '.join(selected_dbs)} into '{new_db_name}'")

def main():
    """
    Main entry point of the script.
    """
    try:
        with open("config.toml", "rb") as f:
            config = tomli.load(f)
    except FileNotFoundError:
        print("Error: config.toml not found.")
        return

    db_configs = config.get("database", {})
    connections = {}

    print("Attempting to connect to databases...")
    for db_name, db_params in db_configs.items():
        conn = connect_to_db(db_params)
        if conn:
            connections[db_name] = conn
            print(f"  - Successfully connected to '{db_name}'")

    if not connections:
        print("No database connections could be established. Exiting.")
        return

    print("\nAvailable databases:")
    for db_name in connections.keys():
        print(f"- {db_name}")

    selected_dbs_str = input("Enter the names of the databases you'd like to combine, separated by spaces: ")
    selected_dbs = [db.strip() for db in selected_dbs_str.split(' ') if db.strip() in connections]

    if not selected_dbs:
        print("No valid databases selected. Exiting.")
    else:
        new_db_name = input("Enter the name for the new combined database: ")
        if new_db_name:
            create_new_database(new_db_name)
            combine_databases(selected_dbs, new_db_name)
        else:
            print("No name provided for the new database. Exiting.")

    # Clean up connections
    for conn in connections.values():
        conn.close()
    print("\nAll database connections closed.")


if __name__ == "__main__":
    main()
