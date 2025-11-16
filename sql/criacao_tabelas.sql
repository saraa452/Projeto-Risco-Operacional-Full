-- Exemplo de DDL para um banco relacional
CREATE TABLE dim_area (
area_id INTEGER PRIMARY KEY,
area TEXT
);


CREATE TABLE dim_system (
system_id INTEGER PRIMARY KEY,
system TEXT
);


CREATE TABLE dim_date (
date_id INTEGER PRIMARY KEY,
date DATE,
year INTEGER,
month INTEGER,
day INTEGER
);


CREATE TABLE fato_incidentes_operacionais (
incident_id TEXT PRIMARY KEY,
datetime DATETIME,
date DATE,
time TEXT,
area TEXT,
system TEXT,
type_incident TEXT,
duration_minutes INTEGER,
impact_brl REAL,
severity TEXT,
status TEXT,
recurrence_count INTEGER,
customer_id TEXT,
latitude REAL,
longitude REAL,
year_month TEXT,
significant_loss INTEGER
);
