# 🚀 Quick Start - Projeto Risco Operacional

## ⚡ Começar em 2 Minutos

```bash
# 1️⃣ Clonar e entrar no diretório
git clone <repo>
cd Projeto-Risco-Operacional-Full

# 2️⃣ Setup automático (cria venv, instala, gera dados, roda ETL + análises)
chmod +x setup.sh
./setup.sh

# ✅ Pronto! Veja os gráficos em: plots/
```

## 📊 Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `make help` | Mostrar todos os comandos |
| `make setup` | Setup inicial (venv + dependências) |
| `make run-etl` | Rodar pipeline: extração → tratamento → carga |
| `make analyze` | Gerar análises e gráficos |
| `make all` | ETL + Análises |
| `make lint` | Verificar qualidade do código |
| `make format` | Formatar código automaticamente |
| `make test` | Rodar testes |
| `make clean` | Limpar arquivos temporários |

## 🎯 Seus Primeiros 10 Minutos

### 1. Entrar no Ambiente
```bash
source .venv/bin/activate
```

### 2. Ver Dados Gerados
```bash
# Data Warehouse
sqlite3 dw/risk_dw.sqlite ".schema"

# Dados limpos
head -5 dados/clean/incidentes_operacionais_clean.csv

# Gráficos
ls -lah plots/

# Log de execução
tail -20 logs/app.log
```

### 3. Executar Análise Custom
```python
# arquivo_analise.py
import sys
sys.path.insert(0, '.')

import config
from analise.risco_operacional_analysis import load_data, get_top_areas_by_loss

df = load_data()
print(get_top_areas_by_loss(df, top_n=3))
```

## 📚 Documentação por Tópico

### Para Iniciar
- [README.md](README.md) - Overview completo
- [DEVELOPMENT.md](DEVELOPMENT.md) - Setup detalhado
- Este arquivo (quick-start)

### Para Desenvolvedores
- [CONTRIBUTING.md](CONTRIBUTING.md) - Padrões de código
- [etl/README.md](etl/README.md) - Documentação pipeline
- [analise/README.md](analise/README.md) - Documentação análises

### Referência
- [config.py](config.py) - Configurações
- [pyproject.toml](pyproject.toml) - Dependências e ferramentas
- [Makefile](Makefile) - Automação

## 💡 Dicas Úteis

### Regenerar dados de teste
```bash
python gerar_dados_teste.py
make run-etl
```

### Ver logs em tempo real
```bash
tail -f logs/app.log
```

### Validar código antes de commit
```bash
make lint && make test && make format
```

### Explorar Data Warehouse
```bash
sqlite3 dw/risk_dw.sqlite
> SELECT * FROM fato_incidentes_operacionais LIMIT 5;
> SELECT * FROM dim_area;
```

### Jupyter Notebook
```bash
jupyter notebook
# Abrir novo notebook e:
import config
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(config.DATABASE_URL)
df = pd.read_sql_table('fato_incidentes_operacionais', engine)
df.describe()
```

## ❓ FAQ

**P: Posso adicionar meus próprios dados?**  
R: Coloque os CSVs em `dados/` com nomes: `incidentes_operacionais.csv` e `perdas_mensais_por_area.csv`

**P: Como uso em produção?**  
R: Veja [DEVELOPMENT.md#Ambiente](DEVELOPMENT.md) para variáveis de ambiente e banco de dados PostgreSQL

**P: Onde estão os testes?**  
R: Ainda em desenvolvimento. Adicione em `tests/` e rode `make test`

**P: Como contribuir?**  
R: Veja [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔗 Links Úteis

- [Documentação Pandas](https://pandas.pydata.org/docs/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints](https://docs.python.org/3/library/typing.html)

---

**Pronto para começar?** Execute `./setup.sh` e veja a magia acontecer! 🎉
