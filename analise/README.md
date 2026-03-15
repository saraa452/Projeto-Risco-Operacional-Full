# Análise de Risco Operacional

Módulo de análises, KPIs e visualizações de riscos operacionais.

## 📋 Visão Geral

Este módulo executa análises sobre os dados do Data Warehouse para gerar insights e visualizações sobre riscos operacionais bancários.

## 📊 Scripts Disponíveis

### `risco_operacional_analysis.py` - Análise Principal
Script principal que executa todas as análises padrão.

**Execução**:
```bash
python risco_operacional_analysis.py
# ou via Makefile
make analyze
```

**Saídas**:
- Resumo executivo (console)
- KPIs do mês mais recente (console)
- Gráficos em `plots/`:
  - `perdas_por_mes.png` - Série temporal de perdas
  - `distribuicao_severidade.png` - Distribuição de severidade
  - `top_areas_perdas.png` - Ranking de áreas por perda

### `perdas.py` - Gerador de Dados Sintéticos
Script para gerar dados de perdas mensais (útil para testes/demos).

**Execução**:
```bash
python perdas.py --start-month 2024-01-01 --end-month 2025-12-01
```

## 📈 KPIs Calculados

### KPIs Mensais
- **Total de incidentes**: Quantidade de eventos no mês
- **Perdas totais (R$)**: Impacto financeiro agregado
- **Perda média (R$)**: Impacto médio por incidente
- **Perda máxima (R$)**: Maior perda individual
- **Duração média (min)**: MTTR médio
- **Incidentes críticos**: Eventos com severidade crítica
- **Perdas significativas**: Eventos no top 10% de impacto

### Métricas Agregadas
- Distribuição por áreas
- Distribuição por severidade
- Tendências temporais
- Top áreas por impacto

## 📊 Visualizações Geradas

### 1. Perdas por Mês
Gráfico de barras mostrando tendência de perdas operacionais mês a mês.

```
Perdas Operacionais por Mês
│
│     ┌─────┐
│     │  50 │ ┌─────┐
│     │  M  │ │ 45M │ ┌─────┐
│     │  R$ │ │ R$ │ │ 48M │
├─────┼─────┼─────┼─────┼─────┼
  2024-01 2024-02 2024-03
```

### 2. Distribuição de Severidade
Gráfico de barras com contagem de eventos por nível de severidade.

Categorias:
- **Baixa**: Impacto mínimo
- **Média**: Impacto moderado
- **Alta**: Impacto significativo
- **Crítica**: Impacto severo

### 3. Top 10 Áreas por Perdas
Ranking horizontal das áreas com maiores perdas acumuladas.

## 🔍 Como Usar

### 1. Executar Análise Padrão
```bash
python analise/risco_operacional_analysis.py
```

Outputs:
```
════════════════════════════════════════════════════════
📋 RESUMO EXECUTIVO
════════════════════════════════════════════════════════
Período analisado: 2024-01 a 2025-12
Total de incidentes: 5,432
Total de perdas: R$ 1,250,000.00
...
════════════════════════════════════════════════════════

════════════════════════════════════════════════════════
📊 KPIs - MÊS MAIS RECENTE
════════════════════════════════════════════════════════
Total de incidentes: 287
Perdas totais (R$): 125,430.00
...
════════════════════════════════════════════════════════
```

### 2. Integrar em Análises Customizadas

```python
import config
from analise.risco_operacional_analysis import (
    load_data,
    get_top_areas_by_loss,
    calculate_monthly_kpis
)

# Carregar dados
df = load_data()

# Obter top 5 áreas
top_5 = get_top_areas_by_loss(df, top_n=5)
print(top_5)

# Calcular KPIs
kpis = calculate_monthly_kpis(df)
print(f"Total de perdas: R$ {kpis['total_loss_brl']:,.2f}")
```

## 🎨 Configuração de Visualizações

Parâmetros em `config.py`:

```python
# Resolução dos gráficos
PLOT_DPI = 300

# Formato de saída
PLOT_FORMAT = "png"

# Cores
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff7f0e"
}
```

## 📝 Extending para Análises Customizadas

### Criar Nova Análise

1. Crie um novo arquivo em `analise/`:
```python
# analise/minha_analise.py
import config
from analise.risco_operacional_analysis import load_data

def analise_customizada():
    df = load_data()
    # Sua análise aqui
    return resultados
```

2. Execute com:
```bash
python analise/minha_analise.py
```

## 🧪 Troubleshooting

### Nenhum dado disponível
```
Error: Nenhum dado disponível para análise
```
**Solução**: Executar o ETL primeiro:
```bash
make run-etl
```

### Gráficos não salvam
```
Permission denied: plots/
```
**Solução**: Verificar permissões:
```bash
chmod -R 755 plots/
```

### Dados inconsistentes
Consultar logs: `logs/app.log`

## 📚 Referências Adicionais

- [ETL Pipeline](../etl/README.md)
- [Configurações](../config.py)
- [Queries SQL](../sql/consultas_risco.sql)

---

**Última atualização**: 10 de março de 2026
