"""
Script de análise: carrega DW SQLite e calcula KPIs, gera gráficos simples.
"""
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if '__file__' in globals() else os.getcwd()
DB_PATH = os.path.join(BASE_DIR, 'dw', 'risk_dw.sqlite')
engine = create_engine(f'sqlite:///{DB_PATH}')


# KPIs
df = pd.read_sql_table('fato_incidentes_operacionais', engine)


total_incidentes_mes = df[df['year_month'] == df['year_month'].max()].shape[0]
print('Total incidentes mês mais recente:', total_incidentes_mes)


# Total de perdas último mês
perdas_mes = df[df['year_month'] == df['year_month'].max()]['impact_brl'].sum()
print('Perdas (R$) mês mais recente:', perdas_mes)


# MTTR geral
mttr = df['duration_minutes'].mean()
print('MTTR médio (minutos):', round(mttr,2))


# Top sistemas por impacto
top_sistemas = df.groupby('system')['impact_brl'].sum().sort_values(ascending=False).head(10)
print('\nTop sistemas por perda:')
print(top_sistemas)


# Plots básicos
os.makedirs(os.path.join(BASE_DIR, 'plots'), exist_ok=True)


# Perdas por mês
perdas_mes_serie = df.groupby('year_month')['impact_brl'].sum().sort_index()
plt.figure()
perdas_mes_serie.plot(kind='bar')
plt.title('Perdas por mês')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'plots', 'perdas_por_mes.png'))
print('Plot salvo: plots/perdas_por_mes.png')


# Heatmap hora x dia (precisa agrupar por hora e dayofweek)
df['hour'] = pd.to_datetime(df['datetime']).dt.hour
df['dow'] = pd.to_datetime(df['datetime']).dt.dayofweek
pivot = df.pivot_table(index='hour', columns='dow', values='incident_id', aggfunc='count').fillna(0)
plt.figure(figsize=(10,6))
plt.imshow(pivot, aspect='auto')
plt.colorbar()
plt.title('Mapa de calor: incidentes por hora x dia da semana')
plt.xlabel('Dia da semana (0=Segunda)')
plt.ylabel('Hora do dia')
plt.savefig(os.path.join(BASE_DIR, 'plots', 'heatmap_hora_dow.png'))
print('Plot salvo: plots/heatmap_hora_dow.png')
