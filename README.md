# Monitor de Risco Operacional Bancário

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Status: Development](https://img.shields.io/badge/Status-Development-yellow.svg)]()

Sistema completo de monitoramento, análise e visualização de riscos operacionais em instituições bancárias. Implementa um pipeline ETL robusto, data warehouse em SQLite, scripts de análise avançada e dashboard interativo.

## 🎯 Funcionalidades

- **Pipeline ETL**: Extração, transformação e carga de dados operacionais
- **Data Warehouse**: Estrutura Dimensional (DW) otimizada em SQLite
- **Análise de Riscos**: KPIs, métricas de impacto e tendências
- **Visualizações**: Gráficos interativos e relatórios
- **Dashboard**: Interface web interativa com Streamlit

## 📋 Requisitos

- **Python**: 3.9 ou superior
- **Dependências**: Listadas em `requirements.txt`

### Softwares Opcionais
- Docker (para containerização)
- PostgreSQL (para produção)

## 🚀 Início Rápido

### 1. Clonar o Repositório
```bash
git clone <seu-repositorio>
cd Projeto-Risco-Operacional-Full
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Preparar Dados
1. Coloque os arquivos CSV em `dados/`:
   - `incidentes_operacionais.csv`
   - `perdas_mensais_por_area.csv`

2. Execute o pipeline ETL:
```bash
make run-etl
# ou manualmente:
python etl/extracao.py
python etl/tratamento.py
python etl/carga.py
```

### 5. Executar Análises
```bash
make analyze
# ou
python analise/risco_operacional_analysis.py
```

### 6. Iniciar Dashboard
```bash
make dashboard
# ou
streamlit run dashboards/streamlit_app.py
# ou
chmod +x run_dashboard.sh && ./run_dashboard.sh
```

## 📁 Estrutura do Projeto

```
Projeto-Risco-Operacional-Full/
├── .gitignore                 # Arquivos ignorados pelo Git
├── LICENSE                    # Licença do projeto
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências Python
├── pyproject.toml            # Configuração do projeto
├── Makefile                  # Automação de tarefas
│
├── analise/                  # Scripts de análise
│   ├── perdas.py            # Análise de perdas operacionais
│   ├── risco_operacional_analysis.py  # KPIs e métricas principais
│   └── README.md
│
├── dashboards/               # Dashboard Streamlit
│   ├── streamlit_app.py      # Aplicação web interativa
│   └── README.md
│
├── bi/                       # Business Intelligence
│   └── dashboard_instructions.md  # Instruções do dashboard
│
├── dados/                    # Dados (entrada/processamento)
│   └── incidentes.py        # Configuração de dados
│
├── etl/                      # Pipeline ETL
│   ├── extracao.py          # Extração de dados
│   ├── tratamento.py        # Transformação/limpeza
│   └── carga.py             # Carga no data warehouse
│
├── dw/                       # Data Warehouse
│   └── risk_dw.sqlite       # Banco de dados SQLite
│
├── plots/                    # Saída de gráficos
│
└── sql/                      # Scripts SQL
    ├── criacao_tabelas.sql  # Criação da estrutura
    └── consultas_risco.sql  # Consultas principais
```

## 🔧 Configuração

As configurações principais podem ser ajustadas em `config.py`:

```python
# Caminhos
DATA_DIR = "./dados"
DW_DIR = "./dw"
PLOTS_DIR = "./plots"

# Banco de dados
DB_PATH = "./dw/risk_dw.sqlite"

# Logging
LOG_LEVEL = "INFO"
```

## 📊 Uso

### Pipeline Completo
```bash
make run-etl
```

### Apenas Análises
```bash
make analyze
```

### Iniciar Dashboard
```bash
make dashboard
# Abre em http://localhost:8501
```

### Todos os Passos
```bash
make all
```

## 🌐 Dashboard Streamlit

O projeto inclui um **dashboard profissional e interativo** para visualização em tempo real dos riscos operacionais.

### O que o Dashboard oferece

**📈 KPIs e Métricas**
- Total de incidentes
- Total de perdas financeiras
- Incidentes críticos
- MTTR (Mean Time To Recovery)

**📊 Gráficos Interativos**
- **Perdas por Mês**: Tendência temporal com cores gradientes
- **Distribuição de Severidade**: Pizza chart com proporções
- **Top Áreas**: Ranking dinâmico de perda (5-20 registros)
- **Top Sistemas**: Ranking dinâmico de impacto (5-20 registros)
- **Incidentes por Área**: Análise por localização
- **Timeline Diária**: Série temporal de incidentes
- **Duração vs Impacto**: Análise de correlação em scatter plot

**🔧 Filtros Avançados**
- Período customizável (data inicial/final)
- Multiselect de áreas
- Multiselect de severidade (CRÍTICO, ALTO, MÉDIO, BAIXO)
- Multiselect de sistemas

**📋 Tabela de Detalhes**
- Busca em tempo real
- Sorting customizável
- Visualização de todos os incidentes com campos completos

**🎨 Design Responsivo**
- Interface profissional com Streamlit
- Caching automático para performance
- Dark mode support

### Como Usar o Dashboard

```bash
# Opção 1: Via Makefile (Recomendado)
make dashboard

# Opção 2: Direto com Streamlit
streamlit run dashboards/streamlit_app.py

# Opção 3: Via script bash
chmod +x run_dashboard.sh && ./run_dashboard.sh
```


**Documentação completa:** [dashboards/README.md](./dashboards/README.md)

## 🧪 Testes (Em desenvolvimento)

```bash
python -m pytest tests/
```

## � Documentação

- [ETL Pipeline](./etl/README.md)
- [Análise](./analise/README.md)
- [Dashboard Streamlit](./dashboards/README.md)
- [Schema do DW](./sql/criacao_tabelas.sql)

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](./LICENSE) para mais detalhes.

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](../../issues) no repositório.

## 🔮 Roadmap

- [ ] Autenticação e controle de acesso
- [ ] Alertas em tempo real
- [ ] Integração com APIs externas
- [ ] Testes unitários e integração
- [ ] CI/CD Pipeline
- [ ] Containerização (Docker)
- [ ] Deploy em cloud (AWS/Azure/GCP)
