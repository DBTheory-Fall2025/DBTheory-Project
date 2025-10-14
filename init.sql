CREATE USER user1 WITH PASSWORD 'password1';
CREATE USER user2 WITH PASSWORD 'password2';

CREATE DATABASE db1;
GRANT ALL PRIVILEGES ON DATABASE db1 TO user1;

CREATE DATABASE db2;
GRANT ALL PRIVILEGES ON DATABASE db2 TO user2;

\c db1;

CREATE TABLE dummy_table (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

COPY dummy_table(id, name)
FROM '/seed-data/dummy_data.csv'
DELIMITER ','
CSV HEADER;

\c db2;

CREATE TABLE dummy_table (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

COPY dummy_table(id, name)
FROM '/seed-data/dummy_data.csv'
DELIMITER ','
CSV HEADER;
