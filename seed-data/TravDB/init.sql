CREATE TABLE users (
    code INTEGER PRIMARY KEY,
    company VARCHAR(255),
    name VARCHAR(255),
    gender VARCHAR(255),
    age INTEGER
);

CREATE TABLE hotels (
    "travelCode" INTEGER PRIMARY KEY,
    "userCode" INTEGER,
    name VARCHAR(255),
    place VARCHAR(255),
    days INTEGER,
    price DECIMAL,
    total DECIMAL,
    date TIMESTAMP,
    FOREIGN KEY("userCode") REFERENCES users(code)
);

CREATE TABLE flights (
    "travelCode" INTEGER NULL,
    "userCode" INTEGER,
    "fromCity" VARCHAR(255),
    "toCity" VARCHAR(255),
    "flightType" VARCHAR(255),
    price DECIMAL,
    time DECIMAL,
    distance DECIMAL,
    agency VARCHAR(255),
    date DATE,
    FOREIGN KEY("userCode") REFERENCES users(code)
    -- FOREIGN KEY("travelCode") REFERENCES hotels("travelCode") MATCH SIMPLE
);
