import psycopg2
#code is from google
#connecting
conn1 = psycopg2.connect(host="localhost", database="db1", user="user1", password="password1", port="5432")
conn2 = psycopg2.connect(host="remote_host", database="db2", user="user2", password="password2", port="5432")
cursor1 = conn1.cursor()
cursor2 = conn2.cursor()
#queries
cursor1.execute("SELECT * FROM table_in_db1;")
results_db1 = cursor1.fetchall()

cursor2.execute("INSERT INTO table_in_db2 (column1) VALUES ('value');")
conn2.commit() # Commit changes for INSERT/UPDATE/DELETE operations

#closing
cursor1.close()
cursor2.close()
conn1.close()
conn2.close()