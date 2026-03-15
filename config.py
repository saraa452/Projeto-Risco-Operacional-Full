"""
Configurações centralizadas do projeto.

Este módulo define todas as configurações, caminhos e constantes
utilizadas em todo o projeto de análise de risco operacional.
"""

import os
import logging
from pathlib import Path

# ================== DIRETÓRIOS ==================
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "dados"
DW_DIR = BASE_DIR / "dw"
ETL_DIR = BASE_DIR / "etl"
ANALISE_DIR = BASE_DIR / "analise"
SQL_DIR = BASE_DIR / "sql"
PLOTS_DIR = BASE_DIR / "plots"
LOGS_DIR = BASE_DIR / "logs"

# Garantir que os diretórios existem
for dir_path in [DATA_DIR, DW_DIR, PLOTS_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# ================== BANCO DE DADOS ==================
DB_PATH = DW_DIR / "risk_dw.sqlite"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# ================== ARQUIVOS DE ENTRADA ==================
CSV_INCIDENTES = DATA_DIR / "incidentes_operacionais.csv"
CSV_PERDAS = DATA_DIR / "perdas_mensais_por_area.csv"

# ================== LOGGING ==================
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "app.log"

# Configuração do logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ================== PARÂMETROS DO ETL ==================
# Chunk size para processamento em lote
CHUNK_SIZE = 10000

# Encoding dos arquivos
FILE_ENCODING = "utf-8"

# ================== PARÂMETROS DE ANÁLISE ==================
# Datas
RECENT_MONTHS_ANALYSIS = 12
MIN_INCIDENTS_FOR_ANALYSIS = 10

# Impacto (valores em R$)
HIGH_IMPACT_THRESHOLD = 50000
MEDIUM_IMPACT_THRESHOLD = 10000

# ================== PARÂMETROS DE VISUALIZAÇÃO ==================
# DPI para gráficos
PLOT_DPI = 300
PLOT_FORMAT = "png"

# Cores
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff7f0e"
}

# ================== AMBIENTE ==================
# Ambiente: 'development', 'staging', 'production'
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ================== FUNCIONALIDADES ==================
ENABLE_CACHE = True
CACHE_TTL = 3600  # segundos

# Função auxiliar para obter logger
def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger configurado para o módulo.
    
    Args:
        name: Nome do módulo (__name__)
    
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name)
