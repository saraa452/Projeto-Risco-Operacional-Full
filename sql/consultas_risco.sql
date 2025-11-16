-- Top 10 maiores perdas
SELECT incident_id, datetime, area, system, impact_brl
FROM fato_incidentes_operacionais
ORDER BY impact_brl DESC
LIMIT 10;


-- Total de perdas por área no mês atual
SELECT year_month, area, SUM(impact_brl) as total_loss, COUNT(*) as incidents
FROM fato_incidentes_operacionais
GROUP BY year_month, area
ORDER BY year_month DESC, total_loss DESC;


-- MTTR médio por sistema
SELECT system, AVG(duration_minutes) as mttr
FROM fato_incidentes_operacionais
GROUP BY system
ORDER BY mttr DESC;


-- Percentual de incidentes críticos
SELECT (SUM(CASE WHEN severity = 'Crítica' THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) as pct_criticos
FROM fato_incidentes_operacionais;
