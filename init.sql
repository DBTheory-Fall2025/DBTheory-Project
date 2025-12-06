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
    "speed" INTEGER
);

CREATE TABLE "addr1" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "address" INTEGER,
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

CREATE USER travdb3_user WITH PASSWORD 'travdb3_password';
CREATE DATABASE travdb3;
GRANT ALL PRIVILEGES ON DATABASE travdb3 TO travdb3_user;

\c travdb3

-- Contents from init.sql to create schema
CREATE TABLE "Travel3" (
    "TravelOptions" VARCHAR(255) PRIMARY KEY,
    "dist" INTEGER,
    "speed" INTEGER
);


CREATE TABLE "addr3" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "address" INTEGER,
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
    "speed" INTEGER
);

CREATE TABLE "addr2" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "address" INTEGER,
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

CREATE USER parceldata_user WITH PASSWORD 'parceldata_password';
CREATE DATABASE parceldata;
GRANT ALL PRIVILEGES ON DATABASE parceldata TO parceldata_user;

\c parceldata

-- Contents from init.sql to create schema

CREATE TABLE enhanced_ownership_summary (
    state VARCHAR(2),
    county VARCHAR(100),
    geoid VARCHAR(50),

    parcel_count INT,
    enhanced_ownership_count INT,
    eo_records_matched INT,
    eo_coverage_pct DECIMAL(6,3),

    max_eo_lastrefresh DATE,
    ll_uuid VARCHAR(100),
    attom_id VARCHAR(100),

    eo_geoid VARCHAR(50),
    eo_lastrefresh DATE,

    eo_owner VARCHAR(255),
    eo_ownerfirst VARCHAR(255),
    eo_ownermiddle VARCHAR(255),
    eo_ownerlast VARCHAR(255),
    eo_ownersuffix VARCHAR(50),

    eo_owner2 VARCHAR(255),
    eo_owner2first VARCHAR(255),
    eo_owner2middle VARCHAR(255),
    eo_owner2last VARCHAR(255),
    eo_owner2suffix VARCHAR(50),

    eo_owner3 VARCHAR(255),
    eo_owner3first VARCHAR(255),
    eo_owner3middle VARCHAR(255),
    eo_owner3suffix VARCHAR(50),
    eo_owner3last VARCHAR(255),

    eo_owner4 VARCHAR(255),
    eo_owner4first VARCHAR(255),
    eo_owner4middle VARCHAR(255),
    eo_owner4last VARCHAR(255),
    eo_owner4suffix VARCHAR(50),

    eo_mail_county VARCHAR(255),
    eo_mail_geoid VARCHAR(50),
    eo_mail_address VARCHAR(255),
    eo_mail_addno VARCHAR(50),
    eo_mail_addpref VARCHAR(50),
    eo_mail_addstr VARCHAR(255),
    eo_mail_addstsuf VARCHAR(50),
    eo_mail_adddir VARCHAR(50),
    eo_mail_unitpref VARCHAR(50),
    eo_mail_unit VARCHAR(50),
    eo_mail_city VARCHAR(100),
    eo_mail_state2 VARCHAR(50),
    eo_mail_zip VARCHAR(10),
    eo_mail_zip4 VARCHAR(10),
    eo_mail_carte VARCHAR(50),
    eo_mail_addressinfoformat VARCHAR(100),

    eo_deedowner VARCHAR(255),
    eo_deedownerfirst VARCHAR(255),
    eo_deedownermiddle VARCHAR(255),
    eo_deedownerlast VARCHAR(255),
    eo_deedownersuffix VARCHAR(50),

    eo_deedowner2 VARCHAR(255),
    eo_deedowner2first VARCHAR(255),
    eo_deedowner2middle VARCHAR(255),
    eo_deedowner2last VARCHAR(255),
    eo_deedowner2suffix VARCHAR(50),

    eo_deedowner3 VARCHAR(255),
    eo_deedowner3first VARCHAR(255),
    eo_deedowner3middle VARCHAR(255),
    eo_deedowner3last VARCHAR(255),
    eo_deedowner3suffix VARCHAR(50),

    eo_deedowner4 VARCHAR(255),
    eo_deedowner4first VARCHAR(255),
    eo_deedowner4middle VARCHAR(255),
    eo_deedowner4last VARCHAR(255),
    eo_deedowner4suffix VARCHAR(50)
);

CREATE TABLE matched_address (
    state VARCHAR(2),
    county VARCHAR(100),
    geoid VARCHAR(50),

    address_count VARCHAR(20),
    total_rows VARCHAR(20),

    ll_uuid VARCHAR(100),
    a_id VARCHAR(100),

    a_address VARCHAR(255),
    a_saddno VARCHAR(50),
    a_saddpref VARCHAR(50),
    a_saddstr VARCHAR(255),
    a_saddsttyp VARCHAR(50),
    a_saddstsuf VARCHAR(50),
    a_sunit VARCHAR(50),

    a_szip5 VARCHAR(10),
    a_szip VARCHAR(20),
    a_carte VARCHAR(50),
    a_crtype VARCHAR(50),
    a_scity VARCHAR(100),
    a_state2 VARCHAR(50),
    a_county VARCHAR(100),

    a_delvseqno VARCHAR(50),
    a_usps_elotseq VARCHAR(50),
    a_usps_elotsort VARCHAR(50),
    a_resbus VARCHAR(50),
    a_pmbdesc VARCHAR(50),
    a_pmbno VARCHAR(50),

    a_dpv_confirm VARCHAR(50),
    a_dpv_footnotes VARCHAR(255),
    a_default_match VARCHAR(50),
    a_lacsflag VARCHAR(50),
    a_usps_vacancy VARCHAR(50),
    a_nostats VARCHAR(50),
    a_error_code VARCHAR(50),
    a_extrainfo VARCHAR(255),
    a_dpv_type VARCHAR(50),

    a_geocodetype VARCHAR(50),
    a_moddate DATE,

    a_census_blockgroup VARCHAR(20),

    a_lat DECIMAL(10,6),
    a_lon DECIMAL(10,6),

    a_geoid VARCHAR(50)
);

CREATE TABLE "MatchBuildFootPrints" (
    ed_geoid VARCHAR(50),
    State VARCHAR(2),
    County VARCHAR(100),
    parcels INT,
    pct_bldgs_matched DECIMAL(6,3),
    buildings INT,
    ed_str_uuid_pct DECIMAL(6,3),
    ed_bld_uuid_pct DECIMAL(6,3),
    ed_geoid_pct DECIMAL(6,3),
    ed_source_pct DECIMAL(6,3),
    ed_source_date_pct DECIMAL(6,3),
    d_bldg_footprint_sqft_pct DECIMAL(10,3),
    ed_largest_pct DECIMAL(6,3),
    ed_lat_pct DECIMAL(10,6),
    ed_lon_pct DECIMAL(10,6),
    wkb_geometry_pct DECIMAL(10,3),
    ed_max_height_pct DECIMAL(10,3),
    ed_mean_height_pct DECIMAL(10,3),
    ed_max_object_height_pct DECIMAL(10,3),
    ed_lag_pct DECIMAL(10,3),
    ed_hag_pct DECIMAL(10,3),
    ed_mean_elevation_pct DECIMAL(10,3),
    ed_mean_slope_pct DECIMAL(10,3),
    ed_stories_pct DECIMAL(10,3),
    ed_gross_area_pct DECIMAL(14,3),
    ed_volume_pct DECIMAL(16,3)
);

CREATE TABLE nationwide_coverage_metrics (
    state VARCHAR(2),
    county VARCHAR(100),
    census_city VARCHAR(200),
    geoid VARCHAR(50),
    last_refresh DATE,
    parcel_count BIGINT,

    ogc_fid_pct DECIMAL(6,2),
    geoid_pct DECIMAL(6,2),
    parcelnumb_pct DECIMAL(6,2),
    parcelnumb_no_formatting_pct DECIMAL(6,2),
    state_parcelnumb_pct DECIMAL(6,2),
    account_number_pct DECIMAL(6,2),
    tax_id_pct DECIMAL(6,2),
    alt_parcelnumb1_pct DECIMAL(6,2),
    alt_parcelnumb2_pct DECIMAL(6,2),
    alt_parcelnumb3_pct DECIMAL(6,2),

    usecode_pct DECIMAL(6,2),
    usedesc_pct DECIMAL(6,2),
    zoning_pct DECIMAL(6,2),
    zoning_description_pct DECIMAL(6,2),
    zoning_type_pct DECIMAL(6,2),
    zoning_subtype_pct DECIMAL(6,2),
    zoning_code_link_pct DECIMAL(6,2),
    zoning_id_pct DECIMAL(6,2),

    struct_pct DECIMAL(6,2),
    structno_pct DECIMAL(6,2),
    yearbuilt_pct DECIMAL(6,2),
    numstories_pct DECIMAL(6,2),
    numunits_pct DECIMAL(6,2),
    numrooms_pct DECIMAL(6,2),
    structstyle_pct DECIMAL(6,2),

    parvaltype_pct DECIMAL(6,2),
    improvval_pct DECIMAL(6,2),
    landval_pct DECIMAL(6,2),
    parval_pct DECIMAL(6,2),
    agval_pct DECIMAL(6,2),
    homestead_exemption_pct DECIMAL(6,2),
    saleprice_pct DECIMAL(6,2),
    saledate_pct DECIMAL(6,2),
    taxamt_pct DECIMAL(6,2),
    taxyear_pct DECIMAL(6,2),

    owntype_pct DECIMAL(6,2),
    owner_pct DECIMAL(6,2),
    unmodified_owner_pct DECIMAL(6,2),
    ownfrst_pct DECIMAL(6,2),
    ownlast_pct DECIMAL(6,2),
    owner2_pct DECIMAL(6,2),
    owner3_pct DECIMAL(6,2),
    owner4_pct DECIMAL(6,2),
    previous_owner_pct DECIMAL(6,2),

    mailadd_pct DECIMAL(6,2),
    mail_address2_pct DECIMAL(6,2),
    careof_pct DECIMAL(6,2),
    mail_addno_pct DECIMAL(6,2),
    mail_addpref_pct DECIMAL(6,2),
    mail_addstr_pct DECIMAL(6,2),
    mail_addsttyp_pct DECIMAL(6,2),
    mail_addstsuf_pct DECIMAL(6,2),
    mail_unit_pct DECIMAL(6,2),
    mail_city_pct DECIMAL(6,2),
    mail_state2_pct DECIMAL(6,2),
    mail_zip_pct DECIMAL(6,2),
    mail_country_pct DECIMAL(6,2),
    mail_urbanization_pct DECIMAL(6,2),
    original_mailing_address_pct DECIMAL(6,2),

    address_pct DECIMAL(6,2),
    address2_pct DECIMAL(6,2),
    saddno_pct DECIMAL(6,2),
    saddpref_pct DECIMAL(6,2),
    saddstr_pct DECIMAL(6,2),
    saddsttyp_pct DECIMAL(6,2),
    saddstsuf_pct DECIMAL(6,2),
    sunit_pct DECIMAL(6,2),
    scity_pct DECIMAL(6,2),
    original_address_pct DECIMAL(6,2),
    city_pct DECIMAL(6,2),
    county_pct DECIMAL(6,2),
    state2_pct DECIMAL(6,2),
    szip_pct DECIMAL(6,2),
    szip5_pct DECIMAL(6,2),
    urbanization_pct DECIMAL(6,2),

    ll_address_count_pct DECIMAL(6,2),
    location_name_pct DECIMAL(6,2),
    address_source_pct DECIMAL(6,2),

    legaldesc_pct DECIMAL(6,2),
    plat_pct DECIMAL(6,2),
    book_pct DECIMAL(6,2),
    page_pct DECIMAL(6,2),
    block_pct DECIMAL(6,2),
    lot_pct DECIMAL(6,2),
    neighborhood_pct DECIMAL(6,2),
    neighborhood_code_pct DECIMAL(6,2),
    subdivision_pct DECIMAL(6,2),

    lat_pct DECIMAL(6,2),
    lon_pct DECIMAL(6,2),

    fema_flood_zone_pct DECIMAL(6,2),
    fema_flood_zone_subtype_pct DECIMAL(6,2),
    fema_flood_zone_raw_pct DECIMAL(6,2),
    fema_flood_zone_data_date_pct DECIMAL(6,2),

    qoz_pct DECIMAL(6,2),
    qoz_tract_pct DECIMAL(6,2),

    census_tract_pct DECIMAL(6,2),
    census_block_pct DECIMAL(6,2),
    census_blockgroup_pct DECIMAL(6,2),
    census_zcta_pct DECIMAL(6,2),
    census_elementary_school_district_pct DECIMAL(6,2),
    census_secondary_school_district_pct DECIMAL(6,2),
    census_unified_school_district_pct DECIMAL(6,2),

    ll_last_refresh_pct DECIMAL(6,2),
    sourceurl_pct DECIMAL(6,2),

    recrdareatx_pct DECIMAL(6,2),
    recrdareano_pct DECIMAL(6,2),
    deeded_acres_pct DECIMAL(6,2),
    gisacre_pct DECIMAL(6,2),
    sqft_pct DECIMAL(6,2),
    ll_gisacre_pct DECIMAL(6,2),
    ll_gissqft_pct DECIMAL(6,2),
    ll_bldg_footprint_sqft_pct DECIMAL(6,2),
    ll_bldg_count_pct DECIMAL(6,2),

    cdl_raw_pct DECIMAL(6,2),
    cdl_majority_category_pct DECIMAL(6,2),
    cdl_majority_percent_pct DECIMAL(6,2),
    cdl_date_pct DECIMAL(6,2),

    plss_township_pct DECIMAL(6,2),
    plss_section_pct DECIMAL(6,2),
    plss_range_pct DECIMAL(6,2),
    reviseddate_pct DECIMAL(6,2),
    path_pct DECIMAL(6,2),
    ll_stable_id_pct DECIMAL(6,2),
    ll_uuid_pct DECIMAL(6,2),
    ll_stack_uuid_pct DECIMAL(6,2),
    ll_row_parcel_pct DECIMAL(6,2),
    ll_updated_at_pct DECIMAL(6,2),

    precisely_id_pct DECIMAL(6,2),
    placekey_pct DECIMAL(6,2),

    dpv_status_pct DECIMAL(6,2),
    dpv_codes_pct DECIMAL(6,2),
    dpv_notes_pct DECIMAL(6,2),
    dpv_type_pct DECIMAL(6,2),
    cass_errorno_pct DECIMAL(6,2),
    rdi_pct DECIMAL(6,2),
    usps_vacancy_pct DECIMAL(6,2),
    usps_vacancy_date_pct DECIMAL(6,2),

    padus_public_access_pct DECIMAL(6,2),

    lbcs_activity_pct DECIMAL(6,2),
    lbcs_activity_desc_pct DECIMAL(6,2),
    lbcs_function_pct DECIMAL(6,2),
    lbcs_function_desc_pct DECIMAL(6,2),
    lbcs_structure_pct DECIMAL(6,2),
    lbcs_structure_desc_pct DECIMAL(6,2),
    lbcs_site_pct DECIMAL(6,2),
    lbcs_site_desc_pct DECIMAL(6,2),
    lbcs_ownership_pct DECIMAL(6,2),
    lbcs_ownership_desc_pct DECIMAL(6,2),

    housing_affordability_index_pct DECIMAL(6,2),
    population_density_pct DECIMAL(6,2),
    population_growth_past_5_years_pct DECIMAL(6,2),
    population_growth_next_5_years_pct DECIMAL(6,2),
    housing_growth_past_5_years_pct DECIMAL(6,2),
    housing_growth_next_5_years_pct DECIMAL(6,2),
    household_income_growth_next_5_years_pct DECIMAL(6,2),
    median_household_income_pct DECIMAL(6,2),

    fema_nri_risk_rating_pct DECIMAL(6,2),
    transmission_line_distance_pct DECIMAL(10,2),
    roughness_rating_pct DECIMAL(10,2),
    highest_parcel_elevation_pct DECIMAL(10,2),
    lowest_parcel_elevation_pct DECIMAL(10,2)
);

CREATE TABLE zoning_coverage_summary (
    geoid VARCHAR(50),
    state VARCHAR(2),
    county VARCHAR(100),
    city VARCHAR(200),
    path VARCHAR(500),

    last_refresh DATE,

    parcels_total BIGINT,
    parcels_in_zone BIGINT,
    zones_total BIGINT,
    distinct_municipalities INT,

    last_date_modified DATE,

    ogc_fid_pct DECIMAL(6,2),
    zoning_id_pct DECIMAL(6,2),
    municipality_id_pct DECIMAL(6,2),
    municipality_name_pct DECIMAL(6,2),

    zoning_pct DECIMAL(6,2),
    zoning_description_pct DECIMAL(6,2),
    zoning_type_pct DECIMAL(6,2),
    zoning_subtype_pct DECIMAL(6,2),

    zoning_guide_pct DECIMAL(6,2),
    zoning_code_link_pct DECIMAL(6,2),

    permitted_land_uses_pct DECIMAL(6,2),
    land_use_flags_permitted_pct DECIMAL(6,2),
    land_use_flags_conditional_pct DECIMAL(6,2),

    min_lot_area_sq_ft_pct DECIMAL(6,2),
    min_lot_width_ft_pct DECIMAL(6,2),
    max_building_height_ft_pct DECIMAL(6,2),
    max_far_pct DECIMAL(6,2),
    max_coverage_pct_pct DECIMAL(6,2),

    min_front_setback_ft_pct DECIMAL(6,2),
    min_rear_setback_ft_pct DECIMAL(6,2),
    max_impervious_coverage_pct_pct DECIMAL(6,2),
    min_side_setback_ft_pct DECIMAL(6,2),
    min_landscaped_space_pct_pct DECIMAL(6,2),
    min_open_space_pct_pct DECIMAL(6,2),
    max_density_du_per_acre_pct DECIMAL(6,2),

    zoning_data_date_pct DECIMAL(6,2),
    path_pct DECIMAL(6,2),
    centroid_pct DECIMAL(6,2)
);

CREATE TABLE state_parcel_coverage (
    state VARCHAR(2),
    parcel_count BIGINT,
    county_count INT,

    ogc_fid_pct DECIMAL(6,2),
    geoid_pct DECIMAL(6,2),
    parcelnumb_pct DECIMAL(6,2),
    parcelnumb_no_formatting_pct DECIMAL(6,2),
    state_parcelnumb_pct DECIMAL(6,2),
    account_number_pct DECIMAL(6,2),
    tax_id_pct DECIMAL(6,2),
    alt_parcelnumb1_pct DECIMAL(6,2),
    alt_parcelnumb2_pct DECIMAL(6,2),
    alt_parcelnumb3_pct DECIMAL(6,2),

    usecode_pct DECIMAL(6,2),
    usedesc_pct DECIMAL(6,2),
    zoning_pct DECIMAL(6,2),
    zoning_description_pct DECIMAL(6,2),
    zoning_type_pct DECIMAL(6,2),
    zoning_subtype_pct DECIMAL(6,2),
    zoning_code_link_pct DECIMAL(6,2),
    zoning_id_pct DECIMAL(6,2),

    struct_pct DECIMAL(6,2),
    structno_pct DECIMAL(6,2),
    yearbuilt_pct DECIMAL(6,2),
    numstories_pct DECIMAL(6,2),
    numunits_pct DECIMAL(6,2),
    numrooms_pct DECIMAL(6,2),
    structstyle_pct DECIMAL(6,2),

    parvaltype_pct DECIMAL(6,2),
    improvval_pct DECIMAL(6,2),
    landval_pct DECIMAL(6,2),
    parval_pct DECIMAL(6,2),
    agval_pct DECIMAL(6,2),
    homestead_exemption_pct DECIMAL(6,2),
    saleprice_pct DECIMAL(6,2),
    saledate_pct DECIMAL(6,2),
    taxamt_pct DECIMAL(6,2),
    taxyear_pct DECIMAL(6,2),

    owntype_pct DECIMAL(6,2),
    owner_pct DECIMAL(6,2),
    unmodified_owner_pct DECIMAL(6,2),
    ownfrst_pct DECIMAL(6,2),
    ownlast_pct DECIMAL(6,2),
    owner2_pct DECIMAL(6,2),
    owner3_pct DECIMAL(6,2),
    owner4_pct DECIMAL(6,2),
    previous_owner_pct DECIMAL(6,2),

    mailadd_pct DECIMAL(6,2),
    mail_address2_pct DECIMAL(6,2),
    careof_pct DECIMAL(6,2),
    mail_addno_pct DECIMAL(6,2),
    mail_addpref_pct DECIMAL(6,2),
    mail_addstr_pct DECIMAL(6,2),
    mail_addsttyp_pct DECIMAL(6,2),
    mail_addstsuf_pct DECIMAL(6,2),
    mail_unit_pct DECIMAL(6,2),
    mail_city_pct DECIMAL(6,2),
    mail_state2_pct DECIMAL(6,2),
    mail_zip_pct DECIMAL(6,2),
    mail_country_pct DECIMAL(6,2),
    mail_urbanization_pct DECIMAL(6,2),
    original_mailing_address_pct DECIMAL(6,2),

    address_pct DECIMAL(6,2),
    address2_pct DECIMAL(6,2),
    saddno_pct DECIMAL(6,2),
    saddpref_pct DECIMAL(6,2),
    saddstr_pct DECIMAL(6,2),
    saddsttyp_pct DECIMAL(6,2),
    saddstsuf_pct DECIMAL(6,2),
    sunit_pct DECIMAL(6,2),
    scity_pct DECIMAL(6,2),
    original_address_pct DECIMAL(6,2),
    city_pct DECIMAL(6,2),
    county_pct DECIMAL(6,2),
    state2_pct DECIMAL(6,2),
    szip_pct DECIMAL(6,2),
    szip5_pct DECIMAL(6,2),
    urbanization_pct DECIMAL(6,2),

    ll_address_count_pct DECIMAL(6,2),
    location_name_pct DECIMAL(6,2),
    address_source_pct DECIMAL(6,2),

    legaldesc_pct DECIMAL(6,2),
    plat_pct DECIMAL(6,2),
    book_pct DECIMAL(6,2),
    page_pct DECIMAL(6,2),
    block_pct DECIMAL(6,2),
    lot_pct DECIMAL(6,2),
    neighborhood_pct DECIMAL(6,2),
    neighborhood_code_pct DECIMAL(6,2),
    subdivision_pct DECIMAL(6,2),

    lat_pct DECIMAL(6,2),
    lon_pct DECIMAL(6,2),

    fema_flood_zone_pct DECIMAL(6,2),
    fema_flood_zone_subtype_pct DECIMAL(6,2),
    fema_flood_zone_raw_pct DECIMAL(6,2),
    fema_flood_zone_data_date_pct DECIMAL(6,2),

    qoz_pct DECIMAL(6,2),
    qoz_tract_pct DECIMAL(6,2),

    census_tract_pct DECIMAL(6,2),
    census_block_pct DECIMAL(6,2),
    census_blockgroup_pct DECIMAL(6,2),
    census_zcta_pct DECIMAL(6,2),
    census_elementary_school_district_pct DECIMAL(6,2),
    census_secondary_school_district_pct DECIMAL(6,2),
    census_unified_school_district_pct DECIMAL(6,2),

    ll_last_refresh_pct DECIMAL(6,2),
    sourceurl_pct DECIMAL(6,2),

    recrdareatx_pct DECIMAL(6,2),
    recrdareano_pct DECIMAL(6,2),
    deeded_acres_pct DECIMAL(6,2),
    gisacre_pct DECIMAL(6,2),
    sqft_pct DECIMAL(6,2),
    ll_gisacre_pct DECIMAL(6,2),
    ll_gissqft_pct DECIMAL(6,2),
    ll_bldg_footprint_sqft_pct DECIMAL(6,2),
    ll_bldg_count_pct DECIMAL(6,2),

    cdl_raw_pct DECIMAL(6,2),
    cdl_majority_category_pct DECIMAL(6,2),
    cdl_majority_percent_pct DECIMAL(6,2),
    cdl_date_pct DECIMAL(6,2),

    plss_township_pct DECIMAL(6,2),
    plss_section_pct DECIMAL(6,2),
    plss_range_pct DECIMAL(6,2),
    reviseddate_pct DECIMAL(6,2),
    path_pct DECIMAL(6,2),
    ll_stable_id_pct DECIMAL(6,2),
    ll_uuid_pct DECIMAL(6,2),
    ll_stack_uuid_pct DECIMAL(6,2),
    ll_row_parcel_pct DECIMAL(6,2),
    ll_updated_at_pct DECIMAL(6,2),

    precisely_id_pct DECIMAL(6,2),
    placekey_pct DECIMAL(6,2),
    dpv_status_pct DECIMAL(6,2),
    dpv_codes_pct DECIMAL(6,2),
    dpv_notes_pct DECIMAL(6,2),
    dpv_type_pct DECIMAL(6,2),
    cass_errorno_pct DECIMAL(6,2),
    rdi_pct DECIMAL(6,2),
    usps_vacancy_pct DECIMAL(6,2),
    usps_vacancy_date_pct DECIMAL(6,2),

    padus_public_access_pct DECIMAL(6,2),

    lbcs_activity_pct DECIMAL(6,2),
    lbcs_activity_desc_pct DECIMAL(6,2),
    lbcs_function_pct DECIMAL(6,2),
    lbcs_function_desc_pct DECIMAL(6,2),
    lbcs_structure_pct DECIMAL(6,2),
    lbcs_structure_desc_pct DECIMAL(6,2),
    lbcs_site_pct DECIMAL(6,2),
    lbcs_site_desc_pct DECIMAL(6,2),
    lbcs_ownership_pct DECIMAL(6,2),
    lbcs_ownership_desc_pct DECIMAL(6,2),

    housing_affordability_index_pct DECIMAL(6,2),
    population_density_pct DECIMAL(6,2),
    population_growth_past_5_years_pct DECIMAL(6,2),
    population_growth_next_5_years_pct DECIMAL(6,2),
    housing_growth_past_5_years_pct DECIMAL(6,2),
    housing_growth_next_5_years_pct DECIMAL(6,2),
    household_income_growth_next_5_years_pct DECIMAL(6,2),
    median_household_income_pct DECIMAL(6,2),

    fema_nri_risk_rating_pct DECIMAL(6,2),
    transmission_line_distance_pct DECIMAL(10,2),
    roughness_rating_pct DECIMAL(10,2),
    highest_parcel_elevation_pct DECIMAL(10,2),
    lowest_parcel_elevation_pct DECIMAL(10,2)
);


CREATE TABLE oh_hamilton (
    geoid VARCHAR(50),
    parcelnumb VARCHAR(100),
    parcelnumb_no_formatting VARCHAR(100),
    state_parcelnumb VARCHAR(100),
    account_number VARCHAR(100),
    tax_id VARCHAR(100),
    alt_parcelnumb1 VARCHAR(100),
    alt_parcelnumb2 VARCHAR(100),
    alt_parcelnumb3 VARCHAR(100),

    usecode VARCHAR(50),
    usedesc VARCHAR(255),
    zoning VARCHAR(100),
    zoning_description VARCHAR(255),
    zoning_type VARCHAR(100),
    zoning_subtype VARCHAR(100),
    zoning_code_link VARCHAR(255),
    zoning_id VARCHAR(100),

    struct VARCHAR(50),
    structno VARCHAR(50),
    yearbuilt INT,
    numstories INT,
    numunits INT,
    numrooms INT,
    structstyle VARCHAR(255),

    parvaltype VARCHAR(100),
    improvval DECIMAL(18,2),
    landval DECIMAL(18,2),
    parval DECIMAL(18,2),
    agval DECIMAL(18,2),
    homestead_exemption VARCHAR(100),

    saleprice DECIMAL(18,2),
    saledate DATE,
    taxamt DECIMAL(18,2),
    taxyear INT,

    owntype VARCHAR(50),
    owner VARCHAR(255),
    unmodified_owner VARCHAR(255),
    ownfrst VARCHAR(255),
    ownlast VARCHAR(255),
    owner2 VARCHAR(255),
    owner3 VARCHAR(255),
    owner4 VARCHAR(255),
    previous_owner VARCHAR(255),

    mailadd VARCHAR(255),
    mail_address2 VARCHAR(255),
    careof VARCHAR(255),
    mail_addno VARCHAR(50),
    mail_addpref VARCHAR(50),
    mail_addstr VARCHAR(255),
    mail_addsttyp VARCHAR(50),
    mail_addstsuf VARCHAR(50),
    mail_unit VARCHAR(100),
    mail_city VARCHAR(100),
    mail_state2 VARCHAR(50),
    mail_zip VARCHAR(20),
    mail_country VARCHAR(100),
    mail_urbanization VARCHAR(100),
    original_mailing_address VARCHAR(255),

    address VARCHAR(255),
    address2 VARCHAR(255),
    saddno VARCHAR(50),
    saddpref VARCHAR(50),
    saddstr VARCHAR(255),
    saddsttyp VARCHAR(50),
    saddstsuf VARCHAR(50),
    sunit VARCHAR(100),
    scity VARCHAR(100),
    original_address VARCHAR(255),
    city VARCHAR(100),
    county VARCHAR(100),
    state2 VARCHAR(50),
    szip VARCHAR(20),
    szip5 VARCHAR(10),
    urbanization VARCHAR(100),

    ll_address_count INT,
    location_name VARCHAR(255),
    address_source VARCHAR(100),

    legaldesc TEXT,
    plat VARCHAR(255),
    book VARCHAR(255),
    page VARCHAR(255),
    block VARCHAR(255),
    lot VARCHAR(255),

    neighborhood VARCHAR(255),
    neighborhood_code VARCHAR(100),
    subdivision VARCHAR(255),

    lat FLOAT,
    lon FLOAT,

    fema_flood_zone VARCHAR(50),
    fema_flood_zone_subtype VARCHAR(50),
    fema_flood_zone_raw VARCHAR(255),
    fema_flood_zone_data_date DATE,
    fema_nri_risk_rating VARCHAR(50),

    qoz BOOLEAN,
    qoz_tract VARCHAR(50),

    census_tract VARCHAR(50),
    census_block VARCHAR(50),
    census_blockgroup VARCHAR(50),
    census_zcta VARCHAR(20),
    census_elementary_school_district VARCHAR(255),
    census_secondary_school_district VARCHAR(255),
    census_unified_school_district VARCHAR(255),

    ll_last_refresh DATE,
    sourceurl VARCHAR(500),

    recrdareatx DECIMAL(18,2),
    recrdareano DECIMAL(18,2),
    deeded_acres DECIMAL(18,4),
    gisacre DECIMAL(18,4),
    sqft INT,
    ll_gisacre DECIMAL(18,4),
    ll_gissqft INT,
    ll_bldg_footprint_sqft INT,
    ll_bldg_count INT,

    cdl_raw VARCHAR(255),
    cdl_majority_category VARCHAR(255),
    cdl_majority_percent DECIMAL(5,2),
    cdl_date DATE,

    plss_township VARCHAR(50),
    plss_section VARCHAR(50),
    plss_range VARCHAR(50),

    reviseddate DATE,
    path VARCHAR(255),

    ll_stable_id VARCHAR(100),
    ll_uuid VARCHAR(100),
    ll_stack_uuid VARCHAR(100),
    ll_row_parcel VARCHAR(100),
    ll_updated_at TIMESTAMP,

    precisely_id VARCHAR(100),
    placekey VARCHAR(100),

    dpv_status VARCHAR(50),
    dpv_codes VARCHAR(255),
    dpv_notes VARCHAR(255),
    dpv_type VARCHAR(50),
    cass_errorno VARCHAR(50),
    rdi VARCHAR(50),
    usps_vacancy VARCHAR(50),
    usps_vacancy_date DATE,

    padus_public_access VARCHAR(50),

    lbcs_activity VARCHAR(50),
    lbcs_activity_desc VARCHAR(255),
    lbcs_function VARCHAR(50),
    lbcs_function_desc VARCHAR(255),
    lbcs_structure VARCHAR(50),
    lbcs_structure_desc VARCHAR(255),
    lbcs_site VARCHAR(50),
    lbcs_site_desc VARCHAR(255),
    lbcs_ownership VARCHAR(50),
    lbcs_ownership_desc VARCHAR(255),

    housing_affordability_index DECIMAL(10,4),
    population_density DECIMAL(10,4),
    population_growth_past_5_years DECIMAL(10,4),
    population_growth_next_5_years DECIMAL(10,4),
    housing_growth_past_5_years DECIMAL(10,4),
    housing_growth_next_5_years DECIMAL(10,4),
    household_income_growth_next_5_years DECIMAL(10,4),
    median_household_income DECIMAL(18,2),

    transmission_line_distance DECIMAL(10,2),
    roughness_rating DECIMAL(10,4),
    highest_parcel_elevation FLOAT,
    lowest_parcel_elevation FLOAT,

    name VARCHAR(255),
    condoname VARCHAR(255),
    phase VARCHAR(100),
    percentown DECIMAL(5,2),

    parcel VARCHAR(100),
    mltown VARCHAR(255),
    parcelid VARCHAR(100),
    grppclid VARCHAR(100),
    pntpclid VARCHAR(100),
    proptyid VARCHAR(100),
    audpclid VARCHAR(100),
    audptyid VARCHAR(100),

    taxdst VARCHAR(100),
    ownnm1 VARCHAR(255),
    ownad1 VARCHAR(255),
    ownad1a VARCHAR(255),
    ownad2 VARCHAR(255),

    splflg VARCHAR(50),
    newflg VARCHAR(50),
    mktcau VARCHAR(50),
    nhbdno VARCHAR(100),
    bankcd VARCHAR(50),
    mlnm1 VARCHAR(255),
    mlnm2 VARCHAR(255),
    numpcl INT,
    salsrc VARCHAR(50),
    salcnv VARCHAR(50),
    deedno VARCHAR(100),
    instty VARCHAR(50),
    div_flag VARCHAR(50),
    forecl_flag VARCHAR(50),

    front_footage DECIMAL(10,2),
    taxes_paid DECIMAL(18,2),
    delq_taxes DECIMAL(18,2),
    convey_no VARCHAR(100),
    owner48 VARCHAR(255),
    exlucode VARCHAR(50),
    taxdst_dis VARCHAR(100),

    ownadcity VARCHAR(100),
    ownadstate VARCHAR(50),
    ownadzip VARCHAR(20),

    apprar VARCHAR(50),
    apprar_dis VARCHAR(50),
    curyr_flag VARCHAR(50),
    school_code_dis VARCHAR(50),
    delq_taxes_pd DECIMAL(18,2),

    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Populating Copy_of_Regrid_Coverage_Report___Enhanced_Ownership___November_12,_2025 from Copy of Regrid Coverage Report - Enhanced Ownership - November 12, 2025.csv
COPY "Copy_of_Regrid_Coverage_Report___Enhanced_Ownership___November_12,_2025" ("state", "county", "geoid", "parcel_count", "enhanced_ownership_count", "eo_records_matched", "eo_coverage_%", "max_eo_lastrefresh", "ll_uuid", "attom_id", "eo_geoid", "eo_lastrefresh", "eo_owner", "eo_ownerfirst", "eo_ownermiddle", "eo_ownerlast", "eo_ownersuffix", "eo_owner2", "eo_owner2first", "eo_owner2middle", "eo_owner2last", "eo_owner2suffix", "eo_owner3", "eo_owner3first", "eo_owner3middle", "eo_owner3suffix", "eo_owner3last", "eo_owner4", "eo_owner4first", "eo_owner4middle", "eo_owner4last", "eo_owner4suffix", "eo_mail_county", "eo_mail_geoid", "eo_mail_address", "eo_mail_addno", "eo_mail_addpref", "eo_mail_addstr", "eo_mail_addstsuf", "eo_mail_adddir", "eo_mail_unitpref", "eo_mail_unit", "eo_mail_city", "eo_mail_state2", "eo_mail_zip", "eo_mail_zip4", "eo_mail_carte", "eo_mail_addressinfoformat", "eo_deedowner", "eo_deedownerfirst", "eo_deedownermiddle", "eo_deedownerlast", "eo_deedownersuffix", "eo_deedowner2", "eo_deedowner2first", "eo_deedowner2middle", "eo_deedowner2last", "eo_deedowner2suffix", "eo_deedowner3", "eo_deedowner3first", "eo_deedowner3middle", "eo_deedowner3last", "eo_deedowner3suffix", "eo_deedowner4", "eo_deedowner4first", "eo_deedowner4middle", "eo_deedowner4last", "eo_deedowner4suffix")
FROM '/seed-data/ParcelData/Copy of Regrid Coverage Report - Enhanced Ownership - November 12, 2025.csv'
DELIMITER ','
CSV HEADER;

-- Populating Copy_of_Regrid_Coverage_Report___State_Summaries___November_12,_2025 from Copy of Regrid Coverage Report - State Summaries - November 12, 2025.csv
COPY "Copy_of_Regrid_Coverage_Report___State_Summaries___November_12,_2025" ("state", "parcel_count", "county_count", "ogc_fid_pct", "geoid_pct", "parcelnumb_pct", "parcelnumb_no_formatting_pct", "state_parcelnumb_pct", "account_number_pct", "tax_id_pct", "alt_parcelnumb1_pct", "alt_parcelnumb2_pct", "alt_parcelnumb3_pct", "usecode_pct", "usedesc_pct", "zoning_pct", "zoning_description_pct", "zoning_type_pct", "zoning_subtype_pct", "zoning_code_link_pct", "zoning_id_pct", "struct_pct", "structno_pct", "yearbuilt_pct", "numstories_pct", "numunits_pct", "numrooms_pct", "structstyle_pct", "parvaltype_pct", "improvval_pct", "landval_pct", "parval_pct", "agval_pct", "homestead_exemption_pct", "saleprice_pct", "saledate_pct", "taxamt_pct", "taxyear_pct", "owntype_pct", "owner_pct", "unmodified_owner_pct", "ownfrst_pct", "ownlast_pct", "owner2_pct", "owner3_pct", "owner4_pct", "previous_owner_pct", "mailadd_pct", "mail_address2_pct", "careof_pct", "mail_addno_pct", "mail_addpref_pct", "mail_addstr_pct", "mail_addsttyp_pct", "mail_addstsuf_pct", "mail_unit_pct", "mail_city_pct", "mail_state2_pct", "mail_zip_pct", "mail_country_pct", "mail_urbanization_pct", "original_mailing_address_pct", "address_pct", "address2_pct", "saddno_pct", "saddpref_pct", "saddstr_pct", "saddsttyp_pct", "saddstsuf_pct", "sunit_pct", "scity_pct", "original_address_pct", "city_pct", "county_pct", "state2_pct", "szip_pct", "szip5_pct", "urbanization_pct", "ll_address_count_pct", "location_name_pct", "address_source_pct", "legaldesc_pct", "plat_pct", "book_pct", "page_pct", "block_pct", "lot_pct", "neighborhood_pct", "neighborhood_code_pct", "subdivision_pct", "lat_pct", "lon_pct", "fema_flood_zone_pct", "fema_flood_zone_subtype_pct", "fema_flood_zone_raw_pct", "fema_flood_zone_data_date_pct", "qoz_pct", "qoz_tract_pct", "census_tract_pct", "census_block_pct", "census_blockgroup_pct", "census_zcta_pct", "census_elementary_school_district_pct", "census_secondary_school_district_pct", "census_unified_school_district_pct", "ll_last_refresh_pct", "sourceurl_pct", "recrdareatx_pct", "recrdareano_pct", "deeded_acres_pct", "gisacre_pct", "sqft_pct", "ll_gisacre_pct", "ll_gissqft_pct", "ll_bldg_footprint_sqft_pct", "ll_bldg_count_pct", "cdl_raw_pct", "cdl_majority_category_pct", "cdl_majority_percent_pct", "cdl_date_pct", "plss_township_pct", "plss_section_pct", "plss_range_pct", "reviseddate_pct", "path_pct", "ll_stable_id_pct", "ll_uuid_pct", "ll_stack_uuid_pct", "ll_row_parcel_pct", "ll_updated_at_pct", "precisely_id_pct", "placekey_pct", "dpv_status_pct", "dpv_codes_pct", "dpv_notes_pct", "dpv_type_pct", "cass_errorno_pct", "rdi_pct", "usps_vacancy_pct", "usps_vacancy_date_pct", "padus_public_access_pct", "lbcs_activity_pct", "lbcs_activity_desc_pct", "lbcs_function_pct", "lbcs_function_desc_pct", "lbcs_structure_pct", "lbcs_structure_desc_pct", "lbcs_site_pct", "lbcs_site_desc_pct", "lbcs_ownership_pct", "lbcs_ownership_desc_pct", "housing_affordability_index_pct", "population_density_pct", "population_growth_past_5_years_pct", "population_growth_next_5_years_pct", "housing_growth_past_5_years_pct", "housing_growth_next_5_years_pct", "household_income_growth_next_5_years_pct", "median_household_income_pct", "fema_nri_risk_rating_pct", "transmission_line_distance_pct", "roughness_rating_pct", "highest_parcel_elevation_pct", "lowest_parcel_elevation_pct")
FROM '/seed-data/ParcelData/Copy of Regrid Coverage Report - State Summaries - November 12, 2025.csv'
DELIMITER ','
CSV HEADER;

-- Populating Copy_of_Regrid_Coverage_Report___Matched_Building_Footprints___November_12,_2025 from Copy of Regrid Coverage Report - Matched Building Footprints - November 12, 2025.csv
COPY "Copy_of_Regrid_Coverage_Report___Matched_Building_Footprints___November_12,_2025" ("ed_geoid", "State", "County", "parcels", "pct_bldgs_matched", "buildings", "ed_str_uuid_pct", "ed_bld_uuid_pct", "ed_geoid_pct", "ed_source_pct", "ed_source_date_pct", "ed_bldg_footprint_sqft_pct", "ed_largest_pct", "ed_lat_pct", "ed_lon_pct", "wkb_geometry_pct", "ed_max_height_pct", "ed_mean_height_pct", "ed_max_object_height_pct", "ed_lag_pct", "ed_hag_pct", "ed_mean_elevation_pct", "ed_mean_slope_pct", "ed_stories_pct", "ed_gross_area_pct", "ed_volume_pct")
FROM '/seed-data/ParcelData/Copy of Regrid Coverage Report - Matched Building Footprints - November 12, 2025.csv'
DELIMITER ','
CSV HEADER;

-- Populating Copy_of_Regrid_Coverage_Report___November_12,_2025 from Copy of Regrid Coverage Report - November 12, 2025.csv
COPY "Copy_of_Regrid_Coverage_Report___November_12,_2025" ("state", "county", "census_city", "geoid", "last_refresh", "parcel_count", "ogc_fid_pct", "geoid_pct", "parcelnumb_pct", "parcelnumb_no_formatting_pct", "state_parcelnumb_pct", "account_number_pct", "tax_id_pct", "alt_parcelnumb1_pct", "alt_parcelnumb2_pct", "alt_parcelnumb3_pct", "usecode_pct", "usedesc_pct", "zoning_pct", "zoning_description_pct", "zoning_type_pct", "zoning_subtype_pct", "zoning_code_link_pct", "zoning_id_pct", "struct_pct", "structno_pct", "yearbuilt_pct", "numstories_pct", "numunits_pct", "numrooms_pct", "structstyle_pct", "parvaltype_pct", "improvval_pct", "landval_pct", "parval_pct", "agval_pct", "homestead_exemption_pct", "saleprice_pct", "saledate_pct", "taxamt_pct", "taxyear_pct", "owntype_pct", "owner_pct", "unmodified_owner_pct", "ownfrst_pct", "ownlast_pct", "owner2_pct", "owner3_pct", "owner4_pct", "previous_owner_pct", "mailadd_pct", "mail_address2_pct", "careof_pct", "mail_addno_pct", "mail_addpref_pct", "mail_addstr_pct", "mail_addsttyp_pct", "mail_addstsuf_pct", "mail_unit_pct", "mail_city_pct", "mail_state2_pct", "mail_zip_pct", "mail_country_pct", "mail_urbanization_pct", "original_mailing_address_pct", "address_pct", "address2_pct", "saddno_pct", "saddpref_pct", "saddstr_pct", "saddsttyp_pct", "saddstsuf_pct", "sunit_pct", "scity_pct", "original_address_pct", "city_pct", "county_pct", "state2_pct", "szip_pct", "szip5_pct", "urbanization_pct", "ll_address_count_pct", "location_name_pct", "address_source_pct", "legaldesc_pct", "plat_pct", "book_pct", "page_pct", "block_pct", "lot_pct", "neighborhood_pct", "neighborhood_code_pct", "subdivision_pct", "lat_pct", "lon_pct", "fema_flood_zone_pct", "fema_flood_zone_subtype_pct", "fema_flood_zone_raw_pct", "fema_flood_zone_data_date_pct", "qoz_pct", "qoz_tract_pct", "census_tract_pct", "census_block_pct", "census_blockgroup_pct", "census_zcta_pct", "census_elementary_school_district_pct", "census_secondary_school_district_pct", "census_unified_school_district_pct", "ll_last_refresh_pct", "sourceurl_pct", "recrdareatx_pct", "recrdareano_pct", "deeded_acres_pct", "gisacre_pct", "sqft_pct", "ll_gisacre_pct", "ll_gissqft_pct", "ll_bldg_footprint_sqft_pct", "ll_bldg_count_pct", "cdl_raw_pct", "cdl_majority_category_pct", "cdl_majority_percent_pct", "cdl_date_pct", "plss_township_pct", "plss_section_pct", "plss_range_pct", "reviseddate_pct", "path_pct", "ll_stable_id_pct", "ll_uuid_pct", "ll_stack_uuid_pct", "ll_row_parcel_pct", "ll_updated_at_pct", "precisely_id_pct", "placekey_pct", "dpv_status_pct", "dpv_codes_pct", "dpv_notes_pct", "dpv_type_pct", "cass_errorno_pct", "rdi_pct", "usps_vacancy_pct", "usps_vacancy_date_pct", "padus_public_access_pct", "lbcs_activity_pct", "lbcs_activity_desc_pct", "lbcs_function_pct", "lbcs_function_desc_pct", "lbcs_structure_pct", "lbcs_structure_desc_pct", "lbcs_site_pct", "lbcs_site_desc_pct", "lbcs_ownership_pct", "lbcs_ownership_desc_pct", "housing_affordability_index_pct", "population_density_pct", "population_growth_past_5_years_pct", "population_growth_next_5_years_pct", "housing_growth_past_5_years_pct", "housing_growth_next_5_years_pct", "household_income_growth_next_5_years_pct", "median_household_income_pct", "fema_nri_risk_rating_pct", "transmission_line_distance_pct", "roughness_rating_pct", "highest_parcel_elevation_pct", "lowest_parcel_elevation_pct")
FROM '/seed-data/ParcelData/Copy of Regrid Coverage Report - November 12, 2025.csv'
DELIMITER ','
CSV HEADER;

-- Populating Copy_of_Regrid_Coverage_Report___Standardized_Zoning___November_12,_2025 from Copy of Regrid Coverage Report - Standardized Zoning - November 12, 2025.csv
COPY "Copy_of_Regrid_Coverage_Report___Standardized_Zoning___November_12,_2025" ("geoid", "state", "county", "city", "path", "last_refresh", "parcels_total", "parcels_in_zone", "zones_total", "distinct_municipalities", "last_date_modified", "ogc_fid_pct", "zoning_id_pct", "municipality_id_pct", "municipality_name_pct", "zoning_pct", "zoning_description_pct", "zoning_type_pct", "zoning_subtype_pct", "zoning_guide_pct", "zoning_code_link_pct", "permitted_land_uses_pct", "land_use_flags_permitted_pct", "land_use_flags_conditional_pct", "min_lot_area_sq_ft_pct", "min_lot_width_ft_pct", "max_building_height_ft_pct", "max_far_pct", "max_coverage_pct_pct", "min_front_setback_ft_pct", "min_rear_setback_ft_pct", "max_impervious_coverage_pct_pct", "min_side_setback_ft_pct", "min_landscaped_space_pct_pct", "min_open_space_pct_pct", "max_density_du_per_acre_pct", "zoning_data_date_pct", "path_pct", "centroid_pct")
FROM '/seed-data/ParcelData/Copy of Regrid Coverage Report - Standardized Zoning - November 12, 2025.csv'
DELIMITER ','
CSV HEADER;

-- Populating Copy_of_Regrid_Coverage_Report___Matched_Addresses___November_12,_2025 from Copy of Regrid Coverage Report - Matched Addresses - November 12, 2025.csv
COPY "Copy_of_Regrid_Coverage_Report___Matched_Addresses___November_12,_2025" ("state", "county", "geoid", "address_count", "total_rows", "ll_uuid", "a_id", "a_address", "a_saddno", "a_saddpref", "a_saddstr", "a_saddsttyp", "a_saddstsuf", "a_sunit", "a_szip5", "a_szip", "a_carte", "a_crtype", "a_scity", "a_state2", "a_county", "a_delvseqno", "a_usps_elotseq", "a_usps_elotsort", "a_resbus", "a_pmbdesc", "a_pmbno", "a_dpv_confirm", "a_dpv_footnotes", "a_default_match", "a_lacsflag", "a_usps_vacancy", "a_nostats", "a_error_code", "a_extrainfo", "a_dpv_type", "a_geocodetype", "a_moddate", "a_census_blockgroup", "a_lat", "a_lon", "a_geoid")
FROM '/seed-data/ParcelData/Copy of Regrid Coverage Report - Matched Addresses - November 12, 2025.csv'
DELIMITER ','
CSV HEADER;

-- Populating oh_hamilton from oh_hamilton.csv
COPY "oh_hamilton" ("geoid", "parcelnumb", "parcelnumb_no_formatting", "state_parcelnumb", "account_number", "tax_id", "alt_parcelnumb1", "alt_parcelnumb2", "alt_parcelnumb3", "usecode", "usedesc", "zoning", "zoning_description", "zoning_type", "zoning_subtype", "zoning_code_link", "zoning_id", "struct", "structno", "yearbuilt", "numstories", "numunits", "numrooms", "structstyle", "parvaltype", "improvval", "landval", "parval", "agval", "homestead_exemption", "saleprice", "saledate", "taxamt", "taxyear", "owntype", "owner", "unmodified_owner", "ownfrst", "ownlast", "owner2", "owner3", "owner4", "previous_owner", "mailadd", "mail_address2", "careof", "mail_addno", "mail_addpref", "mail_addstr", "mail_addsttyp", "mail_addstsuf", "mail_unit", "mail_city", "mail_state2", "mail_zip", "mail_country", "mail_urbanization", "original_mailing_address", "address", "address2", "saddno", "saddpref", "saddstr", "saddsttyp", "saddstsuf", "sunit", "scity", "original_address", "city", "county", "state2", "szip", "szip5", "urbanization", "ll_address_count", "location_name", "address_source", "legaldesc", "plat", "book", "page", "block", "lot", "neighborhood", "neighborhood_code", "subdivision", "lat", "lon", "fema_flood_zone", "fema_flood_zone_subtype", "fema_flood_zone_raw", "fema_flood_zone_data_date", "fema_nri_risk_rating", "qoz", "qoz_tract", "census_tract", "census_block", "census_blockgroup", "census_zcta", "census_elementary_school_district", "census_secondary_school_district", "census_unified_school_district", "ll_last_refresh", "sourceurl", "recrdareatx", "recrdareano", "deeded_acres", "gisacre", "sqft", "ll_gisacre", "ll_gissqft", "ll_bldg_footprint_sqft", "ll_bldg_count", "cdl_raw", "cdl_majority_category", "cdl_majority_percent", "cdl_date", "plss_township", "plss_section", "plss_range", "reviseddate", "path", "ll_stable_id", "ll_uuid", "ll_stack_uuid", "ll_row_parcel", "ll_updated_at", "precisely_id", "placekey", "dpv_status", "dpv_codes", "dpv_notes", "dpv_type", "cass_errorno", "rdi", "usps_vacancy", "usps_vacancy_date", "padus_public_access", "lbcs_activity", "lbcs_activity_desc", "lbcs_function", "lbcs_function_desc", "lbcs_structure", "lbcs_structure_desc", "lbcs_site", "lbcs_site_desc", "lbcs_ownership", "lbcs_ownership_desc", "housing_affordability_index", "population_density", "population_growth_past_5_years", "population_growth_next_5_years", "housing_growth_past_5_years", "housing_growth_next_5_years", "household_income_growth_next_5_years", "median_household_income", "transmission_line_distance", "roughness_rating", "highest_parcel_elevation", "lowest_parcel_elevation", "name", "condoname", "phase", "percentown", "parcel", "mltown", "parcelid", "grppclid", "pntpclid", "proptyid", "audpclid", "audptyid", "taxdst", "ownnm1", "ownad1", "ownad1a", "ownad2", "splflg", "newflg", "mktcau", "nhbdno", "bankcd", "mlnm1", "mlnm2", "numpcl", "salsrc", "salcnv", "deedno", "instty", "div_flag", "forecl_flag", "front_footage", "taxes_paid", "delq_taxes", "convey_no", "owner48", "exlucode", "taxdst_dis", "ownadcity", "ownadstate", "ownadzip", "apprar", "apprar_dis", "curyr_flag", "school_code_dis", "delq_taxes_pd", "date_created")
FROM '/seed-data/ParcelData/oh_hamilton.csv'
DELIMITER ','
CSV HEADER;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO parceldata_user;

