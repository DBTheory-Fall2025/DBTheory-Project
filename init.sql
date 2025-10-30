-- this is an auto-generated file by db_factory/builder.py

CREATE USER cincypothole_user WITH PASSWORD 'cincypothole_password';
CREATE DATABASE cincypothole;
GRANT ALL PRIVILEGES ON DATABASE cincypothole TO cincypothole_user;

\c cincypothole

-- Contents from init.sql to create schema
CREATE TABLE "Pothole_Data_for_Flywheel_010123_090725_1" (
    SR_NUMBER VARCHAR(255) PRIMARY KEY,
    SR_STATUS VARCHAR(255),
    SR_STATUS_FLAG VARCHAR(255),
    SR_TYPE_DESC VARCHAR(255),
    ADDRESS VARCHAR(255)
);

CREATE TABLE "MostPotHoleNeiYear" (
    "NEIGHBORHOOD" VARCHAR(255),
    "yearCreated" INTEGER,
    "totPotHole" INTEGER
);

CREATE TABLE "MostPotHolesNei" (
    "NEIGHBORHOOD" VARCHAR(255),
    "TotNumPot" INTEGER
);

CREATE TABLE "MostPotHolesST" (
    "STREET_NAME" VARCHAR(255),
    "totPotHole" INTEGER
);

CREATE TABLE "MostPotHolesSTNei" (
    "NEIGHBORHOOD" VARCHAR(255),
    "STREET_NAME" VARCHAR(255),
    "TotNumPot" INTEGER
);

CREATE TABLE "MostPotHolesSTYear" (
    "STREET_NAME" VARCHAR(255),
    "yearCreated" INTEGER,
    "totPotHole" INTEGER
);


-- Populating MostPotHolesSTNei from MostPotHolesSTNei.cvs
COPY "MostPotHolesSTNei" ("Unnamed:_0", "NEIGHBORHOOD", "STREET_NAME", "TotNumPot")
FROM '/data/CincyPotHole/MostPotHolesSTNei.cvs'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHoleNeiYear from MostPotHoleNeiYear.cvs
COPY "MostPotHoleNeiYear" ("Unnamed:_0", "NEIGHBORHOOD", "yearCreated", "totPotHole")
FROM '/data/CincyPotHole/MostPotHoleNeiYear.cvs'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHolesSTYear from MostPotHolesSTYear.cvs
COPY "MostPotHolesSTYear" ("Unnamed:_0", "STREET_NAME", "yearCreated", "totPotHole")
FROM '/data/CincyPotHole/MostPotHolesSTYear.cvs'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHolesNei from MostPotHolesNei.cvs
COPY "MostPotHolesNei" ("Unnamed:_0", "NEIGHBORHOOD", "TotNumPot")
FROM '/data/CincyPotHole/MostPotHolesNei.cvs'
DELIMITER ','
CSV HEADER;

-- Populating Pothole_Data_for_Flywheel_010123_090725_1 from Pothole Data for Flywheel 010123-090725 (1).csv
COPY "Pothole_Data_for_Flywheel_010123_090725_1" ("SR_NUMBER", "SR_STATUS", "SR_STATUS_FLAG", "SR_TYPE_DESC", "ADDRESS", "LOCATION", "DATE_CREATED", "PLANNED_END_DATE", "DATE_CLOSED", "Closed_by_Planned_End_Date", "STREET_DIRECTION", "STREET_NO", "STREET_NAME", "ZIPCODE", "NUM_POTHOLES", "METHOD_RECEIVED", "NEIGHBORHOOD", "SNA_NEIGHBORHOOD", "CC_NEIGHBORHOOD", "LATITUDE", "LONGITUDE", "X_COORD", "Y_COORD")
FROM '/data/CincyPotHole/Pothole Data for Flywheel 010123-090725 (1).csv'
DELIMITER ','
CSV HEADER;

-- Populating MostPotHolesST from MostPotHolesST.cvs
COPY "MostPotHolesST" ("Unnamed:_0", "STREET_NAME", "totPotHole")
FROM '/data/CincyPotHole/MostPotHolesST.cvs'
DELIMITER ','
CSV HEADER;

CREATE USER travdb_user WITH PASSWORD 'travdb_password';
CREATE DATABASE travdb;
GRANT ALL PRIVILEGES ON DATABASE travdb TO travdb_user;

\c travdb

-- Contents from init.sql to create schema
CREATE TABLE users (
    code INTEGER PRIMARY KEY,
    company VARCHAR(255),
    name VARCHAR(255),
    gender VARCHAR(255),
    age INTEGER
);

CREATE TABLE flights (
    travelCode INTEGER PRIMARY KEY,
    userCode INTEGER,
    fromCity VARCHAR(255),
    toCity VARCHAR(255),
    flightType VARCHAR(255),
    FOREIGN KEY(userCode) REFERENCES users(code)
);

CREATE TABLE hotels (
    travelCode INTEGER,
    userCode INTEGER,
    name VARCHAR(255),
    place VARCHAR(255),
    days INTEGER,
    FOREIGN KEY(userCode) REFERENCES users(code)
    FOREIGN KEY(travelCode) REFERENCES flights(travelCode)
);


-- Populating users from users.csv
COPY "users" ("code", "company", "name", "gender", "age")
FROM '/data/TravDB/users.csv'
DELIMITER ','
CSV HEADER;

-- Populating hotels from hotels.csv
COPY "hotels" ("travelCode", "userCode", "name", "place", "days", "price", "total", "date")
FROM '/data/TravDB/hotels.csv'
DELIMITER ','
CSV HEADER;

-- Populating flights from flights.csv
COPY "flights" ("travelCode", "userCode", "fromCity", "toCity", "flightType", "price", "time", "distance", "agency", "date")
FROM '/data/TravDB/flights.csv'
DELIMITER ','
CSV HEADER;

CREATE USER hamiltongarb_user WITH PASSWORD 'hamiltongarb_password';
CREATE DATABASE hamiltongarb;
GRANT ALL PRIVILEGES ON DATABASE hamiltongarb TO hamiltongarb_user;

\c hamiltongarb

-- Contents from init.sql to create schema
CREATE TABLE solid_waste_landfills (
    X FLOAT,
    Y FLOAT,
    FID INTEGER PRIMARY KEY,
    permit_id VARCHAR(255),
    fac_name VARCHAR(255)
);

CREATE TABLE waste_summary (
    Origin VARCHAR(255) PRIMARY KEY,
    "Tons Landfilled" FLOAT,
    "Percent Landfilled" VARCHAR(255),
    "Tons Recycled" FLOAT,
    "Percent Recycled" VARCHAR(255)
);

CREATE TABLE waste_targets (
    "Material Sample Origin" VARCHAR(255) PRIMARY KEY,
    "Refuse Season 1 Target" FLOAT,
    "Refuse Season 2 Target" FLOAT,
    "Refuse Actual Collected" FLOAT,
    "Recycling Season 1 Target" FLOAT
);

CREATE TABLE material_composition_1 (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" FLOAT,
    "Margin of Error (%)" FLOAT,
    "Tons/Yr" INTEGER
);

CREATE TABLE material_composition_2 (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" FLOAT,
    "Margin of Error (%)" FLOAT,
    "Tons/Yr" INTEGER
);

CREATE TABLE material_composition_3 (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" FLOAT,
    "Margin of Error (%)" FLOAT,
    "Tons/Yr" INTEGER
);


-- Populating Table_2_2 from Table_2-2.csv
COPY "Table_2_2" ("Material_Sample_Origin", "Refuse_Season_1_Target", "Refuse_Season_2_Target", "Refuse_Actual_Collected", "Recycling_Season_1_Target", "Recycling_Season_2_Target", "Recycling_Actual_Collected", "Grand_Total")
FROM '/data/HamiltonGarb/Table_2-2.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_2_1 from Table_2-1.csv
COPY "Table_2_1" ("Origin", "Tons_Landfilled", "Percent_Landfilled", "Tons_Recycled", "Percent_Recycled")
FROM '/data/HamiltonGarb/Table_2-1.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_3 from Table_4-3.csv
COPY "Table_4_3" ("Material_Category", "Mean_%", "Margin_of_Error_%", "TonsYr")
FROM '/data/HamiltonGarb/Table_4-3.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_2 from Table_4-2.csv
COPY "Table_4_2" ("Material_Category", "Mean_%", "Margin_of_Error_%", "TonsYr")
FROM '/data/HamiltonGarb/Table_4-2.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_1 from Table_4-1.csv
COPY "Table_4_1" ("Material_Category", "Mean_%", "Margin_of_Error_%", "TonsYr")
FROM '/data/HamiltonGarb/Table_4-1.csv'
DELIMITER ','
CSV HEADER;

-- Populating Solid_Waste_Landfill_westV from Solid_Waste_Landfill_westV.csv
COPY "Solid_Waste_Landfill_westV" ("X", "Y", "FID", "permit_id", "fac_name", "issuedate", "expiredate", "sub_desc", "t_c_desc", "statusflag", "perm_type", "latitude", "longitude", "start_date", "end_date", "resp_name", "resp_id", "sludge_ton", "customers", "dist_acres", "des_flow_q", "avg_flow_q", "major_flag", "huc", "rstream", "rs_code")
FROM '/data/HamiltonGarb/Solid_Waste_Landfill_westV.csv'
DELIMITER ','
CSV HEADER;

-- Populating Table_4_1_2 from Table_4-1 (2).csv
COPY "Table_4_1_2" ("Material_Category", "Mean_%", "Margin_of_Error_%", "TonsYr")
FROM '/data/HamiltonGarb/Table_4-1 (2).csv'
DELIMITER ','
CSV HEADER;

