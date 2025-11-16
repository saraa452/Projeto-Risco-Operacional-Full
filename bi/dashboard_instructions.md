# Instruções para montar o Dashboard (Power BI)


Páginas sugeridas:
1. Visão Geral — Cartões com KPIs, linha do tempo de incidentes, tabela TOP perdas
2. Perdas Operacionais — gráficos por área, boxplot, tabela detalhada
3. Falhas de Sistemas — mapa de calor hora x dia, ranking de sistemas por MTTR
4. Previsão — série temporal com previsão ARIMA/Prophet


Slicers/filtros: período (year_month), area, system, severity, status


Datasources: use o SQLite (risk_dw.sqlite) ou os CSVs limpos (`dados/clean/incidentes_operacionais_clean.csv`)


Visuals recomendados: cartões, linhas, barras, matriz/tabela, heatmap (custom visual), mapa (geográfico)
