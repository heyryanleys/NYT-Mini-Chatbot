CREATE TABLE "DailyMessages"
(
    id SERIAL PRIMARY KEY,
    message VARCHAR NOT NULL
);

CREATE TABLE "MonthlyMessages"
(
    id SERIAL PRIMARY KEY,
    message VARCHAR NOT NULL
);

CREATE TABLE "Users"
(
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL,
    birthday DATE
);

CREATE TABLE "DailyMultiplier"
(
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    multiplier INTEGER NOT NULL,
    multiplier_type VARCHAR(50) NOT NULL,
    user_id INTEGER CONSTRAINT fk_user REFERENCES "Users" ON DELETE SET NULL
);

CREATE TABLE "Scores"
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "Users",
    score_time INTERVAL NOT NULL,
    rank INTEGER,
    date DATE NOT NULL,
    multiplier INTEGER,
    points INTEGER DEFAULT 0
);

CREATE TABLE "YearlyMessages"
(
    id SERIAL PRIMARY KEY,
    message VARCHAR NOT NULL
);
