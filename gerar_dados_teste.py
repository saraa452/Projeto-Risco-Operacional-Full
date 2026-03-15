"""
Gerador de dados sintéticos para desenvolvimento/testes.

Cria arquivos CSV de exemplo para testar o pipeline ETL.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Diretórios
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "dados"
DATA_DIR.mkdir(exist_ok=True)

# Configurações
np.random.seed(42)
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
NUM_RECORDS = 1000

# Áreas e Sistemas
AREAS = ["Cartões", "Crédito", "Pagamentos", "Investimentos", "Fraudes", "Canais Digitais"]
SYSTEMS = ["Core Banking", "ATM Network", "Mobile App", "Web Portal", "Payment Gateway"]
SEVERITIES = ["Baixa", "Média", "Alta", "Crítica"]
STATUSES = ["Aberto", "Em Análise", "Resolvido", "Fechado"]

def generate_incidents():
    """Gera arquivo de incidentes operacionais."""
    
    dates = [START_DATE + timedelta(days=int(x)) 
             for x in np.random.uniform(0, (END_DATE - START_DATE).days, NUM_RECORDS)]
    
    data = {
        "incident_id": [f"INC{i:05d}" for i in range(1, NUM_RECORDS + 1)],
        "datetime": dates,
        "date": [d.date() for d in dates],
        "time": [f"{np.random.randint(0, 24):02d}:{np.random.randint(0, 60):02d}:00" for _ in range(NUM_RECORDS)],
        "area": np.random.choice(AREAS, NUM_RECORDS),
        "system": np.random.choice(SYSTEMS, NUM_RECORDS),
        "type_incident": np.random.choice(["Indisponibilidade", "Degradação", "Erro", "Fraude", "Roubo"], NUM_RECORDS),
        "duration_minutes": np.random.randint(5, 480, NUM_RECORDS),
        "impact_brl": np.abs(np.random.gamma(shape=2, scale=10000, size=NUM_RECORDS)).round(2),
        "severity": np.random.choice(SEVERITIES, NUM_RECORDS, p=[0.5, 0.3, 0.15, 0.05]),
        "status": np.random.choice(STATUSES, NUM_RECORDS),
        "recurrence_count": np.random.randint(0, 5, NUM_RECORDS),
        "customer_id": [f"CUST{np.random.randint(1000, 9999)}" for _ in range(NUM_RECORDS)],
        "latitude": np.random.uniform(-33.9, -33.8, NUM_RECORDS),
        "longitude": np.random.uniform(-51.2, -51.1, NUM_RECORDS),
    }
    
    df = pd.DataFrame(data)
    filepath = DATA_DIR / "incidentes_operacionais.csv"
    df.to_csv(filepath, index=False)
    print(f"✓ Gerado: {filepath} ({len(df)} registros)")
    return df

def generate_monthly_losses(df):
    """Gera arquivo agregado de perdas mensais por área."""
    
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["year_month"] = df["datetime"].dt.to_period("M")
    
    monthly = df.groupby(["year_month", "area"]).agg({
        "incident_id": "count",
        "impact_brl": ["sum", "mean", "median"]
    }).reset_index()
    
    monthly.columns = ["year_month", "area", "incidents_count", "total_loss_brl", "avg_loss_brl", "median_loss_brl"]
    monthly["year_month"] = monthly["year_month"].astype(str)
    
    filepath = DATA_DIR / "perdas_mensais_por_area.csv"
    monthly.to_csv(filepath, index=False)
    print(f"✓ Gerado: {filepath} ({len(monthly)} registros)")

if __name__ == "__main__":
    print("Gerando dados sintéticos para testes...")
    print("=" * 60)
    
    df = generate_incidents()
    generate_monthly_losses(df)
    
    print("=" * 60)
    print("✅ Dados sintéticos gerados com sucesso!")
    print(f"Arquivos criados em: {DATA_DIR}")
