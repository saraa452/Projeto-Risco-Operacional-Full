# ETL Pipeline

Pipeline de Extração, Transformação e Carga (ETL) para o sistema de Risco Operacional.

## 📋 Visão Geral

O ETL é dividido em 3 etapas sequenciais:

### 1️⃣ Extração (`extracao.py`)
- **Responsabilidade**: Copiar arquivos CSV brutos de dados
- **Entrada**: Arquivos em `/mnt/data/` (ou variável de ambiente)
- **Saída**: Arquivos em `dados/`
- **Execução**: `python extracao.py`

**Configurações principais** (variáveis de ambiente):
- `SOURCE_INCIDENTES`: Caminho do arquivo de incidentes
- `SOURCE_PERDAS`: Caminho do arquivo de perdas

### 2️⃣ Transformação (`tratamento.py`)
- **Responsabilidade**: Limpar, validar e enriquecer dados
- **Funções**:
  - Remove duplicatas
  - Corrige tipos de dados
  - Normaliza texto
  - Cria colunas derivadas (year_month, flags, etc.)
  - Valida integridade
- **Entrada**: `dados/incidentes_operacionais.csv`
- **Saída**: `dados/clean/incidentes_operacionais_clean.csv`
- **Execução**: `python tratamento.py`

### 3️⃣ Carga (`carga.py`)
- **Responsabilidade**: Populate Data Warehouse SQLite
- **Funções**:
  - Cria dimensões (area, system, date)
  - Cria tabela fato (incidentes)
  - Cria índices paraótimização
  - Valida integridade
- **Entrada**: `dados/clean/incidentes_operacionais_clean.csv`
- **Saída**: `dw/risk_dw.sqlite`
- **Execução**: `python carga.py`

## 🚀 Executar Pipeline Completo

```bash
# Via Makefile (recomendado)
make run-etl

# Ou manualmente
python etl/extracao.py
python etl/tratamento.py
python etl/carga.py
```

## 📊 Schema do Data Warehouse

### Tabelas Criadas

#### `fato_incidentes_operacionais` (Tabela Fato)
```sql
- incident_id (PK)
- datetime
- date, time
- area, system, type_incident
- duration_minutes, impact_brl
- severity (Baixa, Média, Alta, Crítica)
- status
- recurrence_count
- customer_id
- latitude, longitude
- year_month (para análises mensais)
- significant_loss (flag top 10%)
- month, year
```

#### `dim_area` (Dimensão)
```sql
- area_id (PK)
- area (nome)
```

#### `dim_system` (Dimensão)
```sql
- system_id (PK)
- system (nome)
```

#### `dim_date` (Dimensão)
```sql
- date_id (PK)
- date
- year, month, day, quarter, week
```

## 🔧 Configuração

Principais parâmetros em `config.py`:

```python
# Diretórios
DATA_DIR = "./dados"
DW_DIR = "./dw"
DB_PATH = "./dw/risk_dw.sqlite"

# Processamento
CHUNK_SIZE = 10000
FILE_ENCODING = "utf-8"
```

## 📝 Logging

Todos os arquivos utilizam logging configurado em `config.py`:

- Arquivo de log: `logs/app.log`
- Nível padrão: `INFO`
- Saída: Console + Arquivo

## ⚠️ Tratamento de Erros

Cada etapa implementa:

- ✅ Validação de entrada
- ✅ Tratamento de exceções
- ✅ Logging detalhado
- ✅ Código de saída apropriado (0 = sucesso, 1 = erro)

## 🧪 Troubleshooting

### Arquivo de entrada não encontrado
```
Error: Arquivo não encontrado: /mnt/data/incidentes_operacionais.csv
```
**Solução**: Ajuste o caminho ou use variáveis de ambiente:
```bash
export SOURCE_INCIDENTES="/caminho/correto/arquivo.csv"
python etl/extracao.py
```

### Tipos de dados inválidos
```
Column 'impact_brl' convertida para numeric
```
**Solução**: O script trata automaticamente, verificando os logs

### Banco de dados corrompido
```bash
# Limpar e reconstruir
rm dw/risk_dw.sqlite
python etl/carga.py
```

## 📚 Próximos Passos

1. Executar ETL: `make run-etl`
2. Executar análises: `make analyze`
3. Consultar DW: Use SQL em `sql/consultas_risco.sql`

---

**Última atualização**: 10 de março de 2026
