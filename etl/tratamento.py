"""
Tratamento: funciona como um script de limpeza e enriquecimento.
- Remove duplicados
- Conserta tipos
- Cria colunas auxiliares
- Exporta arquivo limpo
"""
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if '__file__' in globals() else os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'dados')
IN_PATH = os.path.join(DATA_DIR, 'incidentes_operacionais.csv')
OUT_DIR = os.path.join(DATA_DIR, 'clean')


os.makedirs(OUT_DIR, exist_ok=True)


# Leitura
df = pd.read_csv(IN_PATH, parse_dates=['datetime'])


# Limpeza básica
# 1. Remover duplicados por incident_id
df = df.drop_duplicates(subset=['incident_id'])


# 2. Preencher severidade faltante com 'Baixa'
df['severity'] = df['severity'].fillna('Baixa')


# 3. Garantir tipos numéricos
for c in ['duration_minutes', 'impact_brl', 'recurrence_count']:
if c in df.columns:
df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)


# 4. Normalizar nomes de area e sistema
if 'area' in df.columns:
df['area'] = df['area'].str.strip().str.title()
if 'system' in df.columns:
df['system'] = df['system'].str.strip().str.title()


# 5. Cria coluna year_month
if 'datetime' in df.columns:
df['year_month'] = df['datetime'].dt.to_period('M').astype(str)


# 6. Flag de perda significativa
df['significant_loss'] = (df['impact_brl'] > df['impact_brl'].quantile(0.90)).astype(int)


# 7. MTTR placeholder — assumimos duration_minutes como MTTR
# Export
out_path = os.path.join(OUT_DIR, 'incidentes_operacionais_clean.csv')
df.to_csv(out_path, index=False)
print('Arquivo limpo salvo em', out_path)
