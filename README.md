Run these for local development

```
pip install -r src/requirements.txt
npm run dev
```

## Database Management

This project uses a database factory to automatically generate and configure databases for testing purposes. You can also connect to existing external databases.

Whenever making changes to dbs, make sure to run

```
npm run down
```

To clean out old databases (dbs will not build if it finds one already exists)

### Adding a New Local Database

To add a new local database that is generated from CSV files, follow these steps:

1.  **Add your data:** Create a new folder in the `data` directory with the name of your new database. Place all your CSV files and a `setup.sql` file in this new folder. The `setup.sql` file should contain the `CREATE TABLE` statements for all the tables you want to create.

2.  **Update the configuration:** Open the `db_factory/config.json` file and add a new entry to the `databases` array. The entry should look like this:

    ```json
    {
      "name": "YourDatabaseName",
      "csv_files": ["file1.csv", "file2.csv"],
      "setup_sql": "setup.sql"
    }
    ```

3.  **Start the services:** Run `docker-compose up --build` to build the services and generate the new database.

### Adding an External Database

To connect to an existing external database, follow these steps:

1.  **Update the configuration:** Open the `db_factory/config.json` file and add a new entry to the `external_databases` array. The entry should look like this:

    ```json
    {
      "name": "YourExternalDatabaseName",
      "host": "your.external.host.com",
      "port": 5432,
      "user": "your_user",
      "password": "your_password",
      "dbname": "your_database_name"
    }
    ```

2.  **Start the services:** Run `docker-compose up --build` to update the application's configuration with the new database connection details.
