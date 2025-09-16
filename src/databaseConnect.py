import psycopg2
import getpass
import os

db_password = os.environ.get("DB_PASSWORD")
if not db_password:
    import getpass
    db_password = getpass.getpass("Enter PostgreSQL password: ")

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password=db_password,
    host="localhost",
    port="5432"
)
cur = conn.cursor()


conn.commit()
cur.close()
conn.close()
