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

CREATE TABLE "Table_2-1" (
    "Origin" VARCHAR(255),
    "Tons Landfilled" DECIMAL,
    "Percent Landfilled" VARCHAR(255),
    "Tons Recycled" DECIMAL,
    "Percent Recycled" VARCHAR(255)
);

CREATE TABLE "Table_2-2" (
    "Material Sample Origin" VARCHAR(255),
    "Refuse Season 1 Target" DECIMAL NULL,
    "Refuse Season 2 Target" DECIMAL NULL,
    "Refuse Actual Collected" DECIMAL NULL,
    "Recycling Season 1 Target" DECIMAL NULL,
    "Recycling Season 2 Target" DECIMAL NULL,
    "Recycling Actual Collected" DECIMAL NULL,
    "Grand Total" DECIMAL NULL
);

CREATE TABLE "Table_4-1" (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" DECIMAL,
    "Margin of Error (%)" DECIMAL,
    "Tons/Yr" INTEGER
);

CREATE TABLE "Table_4-2" (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" DECIMAL,
    "Margin of Error (%)" DECIMAL,
    "Tons/Yr" INTEGER
);

CREATE TABLE "Table_4-3" (
    "Material Category" VARCHAR(255) PRIMARY KEY,
    "Mean (%)" DECIMAL,
    "Margin of Error (%)" DECIMAL,
    "Tons/Yr" INTEGER
);
