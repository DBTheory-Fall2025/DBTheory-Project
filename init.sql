-- this is an auto-generated file by db_factory/builder.py

CREATE USER cincypothole_user WITH PASSWORD 'cincypothole_password';
CREATE DATABASE cincypothole;
GRANT ALL PRIVILEGES ON DATABASE cincypothole TO cincypothole_user;

\c cincypothole

-- Contents from init.sql to create schema
CREATE TABLE "Pothole_Data_for_Flywheel_010123_090725_1" (
    "SR_NUMBER" VARCHAR(255) PRIMARY KEY,
    "SR_STATUS" VARCHAR(255),
    "SR_STATUS_FLAG" VARCHAR(255),
    "SR_TYPE_DESC" VARCHAR(255),
    "ADDRESS" VARCHAR(255),
    "LOCATION" VARCHAR(255),
    "DATE_CREATED" TIMESTAMP,
    "PLANNED_END_DATE" TIMESTAMP,
    "DATE_CLOSED" TIMESTAMP,
    "Closed by Planned End Date" VARCHAR(255),
    "STREET_DIRECTION" VARCHAR(255),
    "STREET_NO" VARCHAR(255),
    "STREET_NAME" VARCHAR(255),
    "ZIPCODE" VARCHAR(20),
    "NUM_POTHOLES" INTEGER,
    "METHOD_RECEIVED" VARCHAR(255),
    "NEIGHBORHOOD" VARCHAR(255),
    "SNA_NEIGHBORHOOD" VARCHAR(255),
    "CC_NEIGHBORHOOD" VARCHAR(255),
    "LATITUDE" DECIMAL,
    "LONGITUDE" DECIMAL,
    "X_COORD" DECIMAL,
    "Y_COORD" DECIMAL
);

CREATE TABLE "MostPotHoleNeiYear" (
    "id" VARCHAR(255) PRIMARY KEY,
    "NEIGHBORHOOD" VARCHAR(255),
    "yearCreated" INTEGER,
    "totPotHole" INTEGER
);

CREATE TABLE "MostPotHolesNei" (
    "id" VARCHAR(255) PRIMARY KEY,
    "NEIGHBORHOOD" VARCHAR(255),
    "TotNumPot" INTEGER
);

CREATE TABLE "MostPotHolesST" (
    "id" VARCHAR(255) PRIMARY KEY,
    "STREET_NAME" VARCHAR(255),
    "totPotHole" INTEGER
);

CREATE TABLE "MostPotHolesSTNei" (
    "id" VARCHAR(255) PRIMARY KEY,
    "NEIGHBORHOOD" VARCHAR(255),
    "STREET_NAME" VARCHAR(255),
    "TotNumPot" INTEGER
);

CREATE TABLE "MostPotHolesSTYear" (
    "id" VARCHAR(255) PRIMARY KEY,
    "STREET_NAME" VARCHAR(255),
    "yearCreated" INTEGER,
    "totPotHole" INTEGER
);


-- Populating MostPotHolesSTNei from MostPotHolesSTNei.cvs
COPY "MostPotHolesSTNei" ("id", "NEIGHBORHOOD", "STREET_NAME", "TotNumPot")
FROM '/seed-data/CincyPotHole/MostPotHolesSTNei.cvs'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHoleNeiYear from MostPotHoleNeiYear.cvs
COPY "MostPotHoleNeiYear" ("id", "NEIGHBORHOOD", "yearCreated", "totPotHole")
FROM '/seed-data/CincyPotHole/MostPotHoleNeiYear.cvs'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHolesSTYear from MostPotHolesSTYear.cvs
COPY "MostPotHolesSTYear" ("id", "STREET_NAME", "yearCreated", "totPotHole")
FROM '/seed-data/CincyPotHole/MostPotHolesSTYear.cvs'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHolesNei from MostPotHolesNei.cvs
COPY "MostPotHolesNei" ("id", "NEIGHBORHOOD", "TotNumPot")
FROM '/seed-data/CincyPotHole/MostPotHolesNei.cvs'
DELIMITER ','
CSV HEADER;

-- Populating Pothole_Data_for_Flywheel_010123_090725_1 from Pothole Data for Flywheel 010123-090725 (1).csv
COPY "Pothole_Data_for_Flywheel_010123_090725_1" ("SR_NUMBER", "SR_STATUS", "SR_STATUS_FLAG", "SR_TYPE_DESC", "ADDRESS", "LOCATION", "DATE_CREATED", "PLANNED_END_DATE", "DATE_CLOSED", "Closed by Planned End Date", "STREET_DIRECTION", "STREET_NO", "STREET_NAME", "ZIPCODE", "NUM_POTHOLES", "METHOD_RECEIVED", "NEIGHBORHOOD", "SNA_NEIGHBORHOOD", "CC_NEIGHBORHOOD", "LATITUDE", "LONGITUDE", "X_COORD", "Y_COORD")
FROM '/seed-data/CincyPotHole/Pothole Data for Flywheel 010123-090725 (1).csv'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHolesST from MostPotHolesST.cvs
COPY "MostPotHolesST" ("id", "STREET_NAME", "totPotHole")
FROM '/seed-data/CincyPotHole/MostPotHolesST.cvs'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cincypothole_user;

CREATE USER travdb_user WITH PASSWORD 'travdb_password';
CREATE DATABASE travdb;
GRANT ALL PRIVILEGES ON DATABASE travdb TO travdb_user;

\c travdb

-- Contents from init.sql to create schema
CREATE TABLE "Travel1" (
    "TravelOptions" VARCHAR(255) PRIMARY KEY,
    "dist" INTEGER,
    "speed" DECIMAL
);

CREATE TABLE "addr1" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "address" VARCHAR(255),
    "income" NUMERIC
);


-- Populating addr1 from addr1.csv
COPY "addr1" ("ID", "address", "income")
FROM '/seed-data/TravDB/addr1.csv'
DELIMITER ','
CSV HEADER;

-- Populating Travel1 from Travel1.csv
COPY "Travel1" ("TravelOptions", "dist", "speed")
FROM '/seed-data/TravDB/Travel1.csv'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO travdb_user;

CREATE USER hamiltongarb_user WITH PASSWORD 'hamiltongarb_password';
CREATE DATABASE hamiltongarb;
GRANT ALL PRIVILEGES ON DATABASE hamiltongarb TO hamiltongarb_user;

\c hamiltongarb

-- Contents from init.sql to create schema
CREATE TABLE "Solid_Waste_Landfill_westV" (
    "X" NUMERIC,
    "Y" NUMERIC,
    "FID" INTEGER,
    "permit_id" TEXT,
    "fac_name" TEXT,
    "issuedate" TEXT,
    "expiredate" TEXT,
    "sub_desc" TEXT,
    "t_c_desc" TEXT,
    "statusflag" TEXT,
    "perm_type" TEXT,
    "latitude" NUMERIC,
    "longitude" NUMERIC,
    "start_date" TEXT,
    "end_date" TEXT,
    "resp_name" TEXT,
    "resp_id" TEXT,
    "sludge_ton" NUMERIC,
    "customers" NUMERIC,
    "dist_acres" NUMERIC,
    "des_flow_q" NUMERIC,
    "avg_flow_q" NUMERIC,
    "major_flag" TEXT,
    "huc" TEXT,
    "rstream" TEXT,
    "rs_code" TEXT
);

CREATE TABLE "Table_2_1" (
    "Origin" VARCHAR(255),
    "Tons Landfilled" DECIMAL,
    "Percent Landfilled" VARCHAR(255),
    "Tons Recycled" DECIMAL,
    "Percent Recycled" VARCHAR(255)
);

CREATE TABLE "Table_2_2" (
    "Material Sample Origin" VARCHAR(255),
    "Refuse Season 1 Target" DECIMAL NULL,
    "Refuse Season 2 Target" DECIMAL NULL,
    "Refuse Actual Collected" DECIMAL NULL,
    "Recycling Season 1 Target" DECIMAL NULL,
    "Recycling Season 2 Target" DECIMAL NULL,
    "Recycling Actual Collected" DECIMAL NULL,
    "Grand Total" DECIMAL NULL
);

CREATE TABLE "Table_4_1" (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" DECIMAL,
    "Margin of Error (%)" DECIMAL,
    "Tons/Yr" INTEGER
);

CREATE TABLE "Table_4_2" (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" DECIMAL,
    "Margin of Error (%)" DECIMAL,
    "Tons/Yr" INTEGER
);

CREATE TABLE "Table_4_3" (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" DECIMAL,
    "Margin of Error (%)" DECIMAL,
    "Tons/Yr" INTEGER
);


-- Populating Table_2_2 from Table_2-2.csv
COPY "Table_2_2" ("Material Sample Origin", "Refuse Season 1 Target", "Refuse Season 2 Target", "Refuse Actual Collected", "Recycling Season 1 Target", "Recycling Season 2 Target", "Recycling Actual Collected", "Grand Total")
FROM '/seed-data/HamiltonGarb/Table_2-2.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_2_1 from Table_2-1.csv
COPY "Table_2_1" ("Origin", "Tons Landfilled", "Percent Landfilled", "Tons Recycled", "Percent Recycled")
FROM '/seed-data/HamiltonGarb/Table_2-1.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_3 from Table_4-3.csv
COPY "Table_4_3" ("Material Category", "Mean (%)", "Margin of Error (%)", "Tons/Yr")
FROM '/seed-data/HamiltonGarb/Table_4-3.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_2 from Table_4-2.csv
COPY "Table_4_2" ("Material Category", "Mean (%)", "Margin of Error (%)", "Tons/Yr")
FROM '/seed-data/HamiltonGarb/Table_4-2.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_1 from Table_4-1.csv
COPY "Table_4_1" ("Material Category", "Mean (%)", "Margin of Error (%)", "Tons/Yr")
FROM '/seed-data/HamiltonGarb/Table_4-1.csv'
DELIMITER ','
CSV HEADER;

-- Populating Solid_Waste_Landfill_westV from Solid_Waste_Landfill_westV.csv
COPY "Solid_Waste_Landfill_westV" ("X", "Y", "FID", "permit_id", "fac_name", "issuedate", "expiredate", "sub_desc", "t_c_desc", "statusflag", "perm_type", "latitude", "longitude", "start_date", "end_date", "resp_name", "resp_id", "sludge_ton", "customers", "dist_acres", "des_flow_q", "avg_flow_q", "major_flag", "huc", "rstream", "rs_code")
FROM '/seed-data/HamiltonGarb/Solid_Waste_Landfill_westV.csv'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hamiltongarb_user;

CREATE USER travdb4address_user WITH PASSWORD 'travdb4address_password';
CREATE DATABASE travdb4address;
GRANT ALL PRIVILEGES ON DATABASE travdb4address TO travdb4address_user;

\c travdb4address

-- Contents from init.sql to create schema
CREATE TABLE "Travel1" (
    "TravelOptions" VARCHAR(255) PRIMARY KEY,
    "dist" INTEGER,
    "speed" DECIMAL
);

CREATE TABLE "addr1" (
    "ID" INTEGER PRIMARY KEY,
    "homeNum" INTEGER, 
    "street" VARCHAR(255), 
    "city" VARCHAR(255), 
    "state"  VARCHAR(2),
    "zip" INTEGER,
    "income" DECIMAL
);

CREATE TABLE "trips" (
    "trip" INTEGER PRIMARY KEY,
    "dest" INTEGER,
    "TravelOptions" INTEGER,
    "start" INTEGER
    
);

-- Populating addr1 from addr1.csv
COPY "addr1" ("ID", "homeNum", "street", "city", "state", "zip", "income")
FROM '/seed-data/TravDB4address/addr1.csv'
DELIMITER ','
CSV HEADER;

-- Populating Travel1 from Travel1.csv
COPY "Travel1" ("TravelOptions", "dist", "speed")
FROM '/seed-data/TravDB4address/Travel1.csv'
DELIMITER ','
CSV HEADER;

-- Populating trips from trips.csv
COPY "trips" ("trip", "dest", "TravelOptions", "start")
FROM '/seed-data/TravDB4address/trips.csv'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO travdb4address_user;

CREATE USER travdb3_user WITH PASSWORD 'travdb3_password';
CREATE DATABASE travdb3;
GRANT ALL PRIVILEGES ON DATABASE travdb3 TO travdb3_user;

\c travdb3

-- Contents from init.sql to create schema
CREATE TABLE "Travel3" (
    "TravelTypes" VARCHAR(255) PRIMARY KEY,
    "TravDist" INTEGER,
    "speed" DECIMAL,
    "cost" INTEGER
);


CREATE TABLE "addr3" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "address" VARCHAR(255),
    "income" NUMERIC
);

-- Populating addr3 from addr3.csv
COPY "addr3" ("ID", "address", "income")
FROM '/seed-data/TravDB3/addr3.csv'
DELIMITER ','
CSV HEADER;

-- Populating Travel3 from Travel3.csv
COPY "Travel3" ("TravelTypes", "TravDist", "speed", "cost")
FROM '/seed-data/TravDB3/Travel3.csv'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO travdb3_user;

CREATE USER travdb2_user WITH PASSWORD 'travdb2_password';
CREATE DATABASE travdb2;
GRANT ALL PRIVILEGES ON DATABASE travdb2 TO travdb2_user;

\c travdb2

-- Contents from init.sql to create schema
CREATE TABLE "Travel2" (
    "TravelOptions" VARCHAR(255) PRIMARY KEY,
    "dist" INTEGER,
    "speed" DECIMAL
);

CREATE TABLE "addr2" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "address" VARCHAR(255),
    "income" NUMERIC
);



-- Populating addr2 from addr2.csv
COPY "addr2" ("ID", "address", "income")
FROM '/seed-data/TravDB2/addr2.csv'
DELIMITER ','
CSV HEADER;

-- Populating Travel2 from Travel2.csv
COPY "Travel2" ("TravelOptions", "dist", "speed")
FROM '/seed-data/TravDB2/Travel2.csv'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO travdb2_user;

