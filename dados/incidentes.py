import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Parameters
n = 1500
np.random.seed(123)
random.seed(123)

areas = ["Cartões", "Crédito", "Pagamentos", "Investimentos", "Fraudes", "Canais Digitais"]
sistemas = ["App", "API Pagamentos", "Core Banking", "Autenticação", "Cartões", "Notificações Push"]
tipos = ["Falha de Sistema", "Erro Humano", "Fraude Interna", "Problema de Processo"]
severidades = ["Baixa", "Média", "Alta", "Crítica"]
status_list = ["Aberto", "Em Tratamento", "Resolvido"]

base_date = datetime(2024, 1, 1)

rows = []
for i in range(1, n+1):
    dt = base_date + timedelta(minutes=random.randint(0, 60*24*365))
    rows.append([
        i,
        dt.strftime("%Y-%m-%d %H:%M:%S"),
        dt.date().isoformat(),
        dt.time().strftime("%H:%M:%S"),
        random.choice(areas),
        random.choice(sistemas),
        random.choice(tipos),
        int(abs(np.random.normal(45, 20))),
        round(abs(np.random.normal(2500, 7000)), 2),
        random.choices(severidades, weights=[0.45, 0.30, 0.20, 0.05])[0],
        random.choices(status_list, weights=[0.15, 0.25, 0.60])[0],
        np.random.poisson(0.8),
        np.random.randint(100000, 999999),
        -23.5 + np.random.normal(0, 0.05),
        -46.6 + np.random.normal(0, 0.05)
    ])

columns = [
    "incident_id", "datetime", "date", "time", "area", "system", "type_incident",
    "duration_minutes", "impact_brl", "severity", "status",
    "recurrence_count", "customer_id", "latitude", "longitude"
]

df = pd.DataFrame(rows, columns=columns)

path = "/mnt/data/incidentes_operacionais.csv"
df.to_csv(path, index=False)

path
