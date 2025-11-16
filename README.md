# Projeto: Monitor de Risco Operacional Bancário


Conteúdo: pipeline ETL, data warehouse em SQLite, scripts de análise e instrução de dashboard.


## Requisitos
- Python 3.9+
- Bibliotecas: ver `requirements.txt`


## Como rodar (local)
1. Coloque os arquivos CSV em `projeto_risco_operacional/dados/` (ou ajuste caminhos nos scripts).
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows
pip install -r requirements.txt
