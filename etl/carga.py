"""
Carga: cria um SQLite data warehouse e grava tabelas dimensionais e fato.
"""
import pandas as pd
import os
from sqlalchemy import create_engine, text


BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if '__file__' in globals() else os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'dados', 'clean')
DB_DIR = os.path.join(BASE_DIR, 'dw')


os.makedirs(DB_DIR, exist_ok=True)


INC_PATH = os.path.join(DATA_DIR, 'incidentes_operacionais_clean.csv')
DB_PATH = os.path.join(DB_DIR, 'risk_dw.sqlite')


# Leitura
df = pd.read_csv(INC_PATH, parse_dates=['datetime'])


engine = create_engine(f'sqlite:///{DB_PATH}')


# Tabela fato: fato_incidentes_operacionais
fact_cols = [
'incident_id', 'datetime', 'date', 'time', 'area', 'system', 'type_incident',
'duration_minutes', 'impact_brl', 'severity', 'status', 'recurrence_count',
'customer_id', 'latitude', 'longitude', 'year_month', 'significant_loss'
]


df_fact = df[fact_cols].copy()


df_fact.to_sql('fato_incidentes_operacionais', engine, if_exists='replace', index=False)


# Dimensões simples
dim_area = df[['area']].drop_duplicates().reset_index(drop=True)
dim_area['area_id'] = dim_area.index + 1
dim_area.to_sql('dim_area', engine, if_exists='replace', index=False)


# dim_sistema
dim_system = df[['system']].drop_duplicates().reset_index(drop=True)
dim_system['system_id'] = dim_system.index + 1
dim_system.to_sql('dim_system', engine, if_exists='replace', index=False)


# dim_data (criar a partir dos datetimes únicos)
unique_dates = pd.to_datetime(df['datetime'].dt.date.unique())
dim_date = pd.DataFrame({'date': unique_dates})
dim_date['date_id'] = dim_date.index + 1
dim_date['year'] = dim_date['date'].dt.year
dim_date['month'] = dim_date['date'].dt.month
dim_date['day'] = dim_date['date'].dt.day
dim_date.to_sql('dim_date', engine, if_exists='replace', index=False)


print('DW criado em', DB_PATH)
