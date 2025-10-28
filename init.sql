-- this is an auto-generated file by db_factory/builder.py

CREATE USER CincyPotHole_user WITH PASSWORD 'CincyPotHole_password';
CREATE DATABASE CincyPotHole;
GRANT ALL PRIVILEGES ON DATABASE CincyPotHole TO CincyPotHole_user;

SET search_path TO CincyPotHole;

COPY MostPotHoleNeiYear
FROM '/data/CincyPotHole/MostPotHoleNeiYear.cvs'
DELIMITER ','
CSV HEADER;

COPY MostPotHolesNei
FROM '/data/CincyPotHole/MostPotHolesNei.cvs'
DELIMITER ','
CSV HEADER;

COPY MostPotHolesST
FROM '/data/CincyPotHole/MostPotHolesST.cvs'
DELIMITER ','
CSV HEADER;

COPY MostPotHolesSTNei
FROM '/data/CincyPotHole/MostPotHolesSTNei.cvs'
DELIMITER ','
CSV HEADER;

COPY MostPotHolesSTYear
FROM '/data/CincyPotHole/MostPotHolesSTYear.cvs'
DELIMITER ','
CSV HEADER;

COPY Pothole Data for Flywheel 010123-090725 (1)
FROM '/data/CincyPotHole/Pothole Data for Flywheel 010123-090725 (1).csv'
DELIMITER ','
CSV HEADER;

CREATE USER HamiltonGarb_user WITH PASSWORD 'HamiltonGarb_password';
CREATE DATABASE HamiltonGarb;
GRANT ALL PRIVILEGES ON DATABASE HamiltonGarb TO HamiltonGarb_user;

SET search_path TO HamiltonGarb;

COPY Solid_Waste_Landfill_westV
FROM '/data/HamiltonGarb/Solid_Waste_Landfill_westV.csv'
DELIMITER ','
CSV HEADER;

COPY Table_2-1
FROM '/data/HamiltonGarb/Table_2-1.csv'
DELIMITER ','
CSV HEADER;

COPY Table_2-2
FROM '/data/HamiltonGarb/Table_2-2.csv'
DELIMITER ','
CSV HEADER;

COPY Table_4-1 (2)
FROM '/data/HamiltonGarb/Table_4-1 (2).csv'
DELIMITER ','
CSV HEADER;

COPY Table_4-1
FROM '/data/HamiltonGarb/Table_4-1.csv'
DELIMITER ','
CSV HEADER;

COPY Table_4-2
FROM '/data/HamiltonGarb/Table_4-2.csv'
DELIMITER ','
CSV HEADER;

COPY Table_4-3
FROM '/data/HamiltonGarb/Table_4-3.csv'
DELIMITER ','
CSV HEADER;

CREATE USER TravDB_user WITH PASSWORD 'TravDB_password';
CREATE DATABASE TravDB;
GRANT ALL PRIVILEGES ON DATABASE TravDB TO TravDB_user;

SET search_path TO TravDB;

COPY flights
FROM '/data/TravDB/flights.csv'
DELIMITER ','
CSV HEADER;

COPY hotels
FROM '/data/TravDB/hotels.csv'
DELIMITER ','
CSV HEADER;

COPY users
FROM '/data/TravDB/users.csv'
DELIMITER ','
CSV HEADER;

