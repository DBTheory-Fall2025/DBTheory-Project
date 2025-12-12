CREATE TABLE "Travel1" (
    "TravelOptions" VARCHAR(255) PRIMARY KEY,
    "dist" INTEGER,
    "speed" INTEGER
);

CREATE TABLE "addr1" (
    "ID" VARCHAR(255) PRIMARY KEY,
    "homeNum" INTEGER, 
    "street" VARCHAR(255), 
    "city" VARCHAR(255), 
    "state"  VARCHAR(2),
    "zip" INTEGER,
    "income" DECIMAL
);
