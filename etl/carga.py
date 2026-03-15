"""
Módulo de Carga - ETL Pipeline

Responsável pela criação e população do Data Warehouse (DW):
- Cria dimensões (área, sistema, data)
- Cria tabela fato (incidentes operacionais)
- Índices e constraints
- Validações de integridade

Típo de execução:
    python etl/carga.py
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Adicionar diretório raiz ao path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from sqlalchemy import create_engine, text, Engine

import config

logger = config.get_logger(__name__)

# Configurações
INPUT_FILE = config.DATA_DIR / "clean" / "incidentes_operacionais_clean.csv"
DB_PATH = config.DB_PATH

# Colunas da tabela fato
FACT_COLUMNS = [
    "incident_id", "datetime", "date", "time", "area", "system",
    "type_incident", "duration_minutes", "impact_brl", "severity",
    "status", "recurrence_count", "customer_id", "latitude",
    "longitude", "year_month", "significant_loss", "month", "year"
]


def create_engine_connection(db_path: Path) -> Optional[Engine]:
    """
    Cria conexão com o banco de dados SQLite.

    Args:
        db_path: Caminho do arquivo SQLite

    Returns:
        Engine do SQLAlchemy ou None se erro
    """
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(f"sqlite:///{db_path}")
        logger.info(f"✓ Conexão com banco de dados estabelecida: {db_path}")
        return engine
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return None


def load_clean_data(filepath: Path) -> Optional[pd.DataFrame]:
    """
    Carrega dados limpos do CSV.

    Args:
        filepath: Caminho do arquivo CSV

    Returns:
        DataFrame ou None se erro
    """
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

        df = pd.read_csv(filepath, parse_dates=["datetime"])
        logger.info(f"✓ Dados carregados: {len(df)} linhas")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return None


def create_fact_table(df: pd.DataFrame, engine: Engine) -> bool:
    """
    Cria e popula tabela fato de incidentes operacionais.

    Args:
        df: DataFrame com dados limpos
        engine: Engine do SQLAlchemy

    Returns:
        True se bem-sucedido
    """
    try:
        # Garantir que todas as colunas necessárias existem
        for col in FACT_COLUMNS:
            if col not in df.columns:
                logger.warning(f"Coluna '{col}' não encontrada, criando com valores nulos")
                df[col] = None

        df_fact = df[FACT_COLUMNS].copy()

        df_fact.to_sql(
            "fato_incidentes_operacionais",
            engine,
            if_exists="replace",
            index=False
        )

        logger.info(f"✓ Tabela fato criada com {len(df_fact)} registros")
        return True

    except Exception as e:
        logger.error(f"Erro ao criar tabela fato: {e}")
        return False


def create_dimension_area(df: pd.DataFrame, engine: Engine) -> bool:
    """
    Cria dimensão de áreas.

    Args:
        df: DataFrame fonte
        engine: Engine do SQLAlchemy

    Returns:
        True se bem-sucedido
    """
    try:
        dim_area = df[["area"]].drop_duplicates().reset_index(drop=True)
        dim_area["area_id"] = range(1, len(dim_area) + 1)

        dim_area.to_sql(
            "dim_area",
            engine,
            if_exists="replace",
            index=False
        )

        logger.info(f"✓ Dimensão 'area' criada com {len(dim_area)} registros")
        return True

    except Exception as e:
        logger.error(f"Erro ao criar dimensão area: {e}")
        return False


def create_dimension_system(df: pd.DataFrame, engine: Engine) -> bool:
    """
    Cria dimensão de sistemas.

    Args:
        df: DataFrame fonte
        engine: Engine do SQLAlchemy

    Returns:
        True se bem-sucedido
    """
    try:
        dim_system = df[["system"]].drop_duplicates().reset_index(drop=True)
        dim_system["system_id"] = range(1, len(dim_system) + 1)

        dim_system.to_sql(
            "dim_system",
            engine,
            if_exists="replace",
            index=False
        )

        logger.info(f"✓ Dimensão 'system' criada com {len(dim_system)} registros")
        return True

    except Exception as e:
        logger.error(f"Erro ao criar dimensão system: {e}")
        return False


def create_dimension_date(df: pd.DataFrame, engine: Engine) -> bool:
    """
    Cria dimensão de data.

    Args:
        df: DataFrame fonte
        engine: Engine do SQLAlchemy

    Returns:
        True se bem-sucedido
    """
    try:
        unique_dates = pd.to_datetime(df["datetime"].dt.date.unique())
        dim_date = pd.DataFrame({"date": unique_dates})
        dim_date["date_id"] = range(1, len(dim_date) + 1)
        dim_date["year"] = dim_date["date"].dt.year
        dim_date["month"] = dim_date["date"].dt.month
        dim_date["day"] = dim_date["date"].dt.day
        dim_date["quarter"] = dim_date["date"].dt.quarter
        dim_date["week"] = dim_date["date"].dt.isocalendar().week

        dim_date.to_sql(
            "dim_date",
            engine,
            if_exists="replace",
            index=False
        )

        logger.info(f"✓ Dimensão 'date' criada com {len(dim_date)} registros")
        return True

    except Exception as e:
        logger.error(f"Erro ao criar dimensão date: {e}")
        return False


def create_indexes(engine: Engine) -> bool:
    """
    Cria índices para otimização de queries.

    Args:
        engine: Engine do SQLAlchemy

    Returns:
        True se bem-sucedido
    """
    try:
        with engine.connect() as conn:
            # Índices na tabela fato
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_fato_area "
                "ON fato_incidentes_operacionais(area)"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_fato_datetime "
                "ON fato_incidentes_operacionais(datetime)"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_fato_impact "
                "ON fato_incidentes_operacionais(impact_brl)"
            ))
            conn.commit()

        logger.info("✓ Índices criados com sucesso")
        return True

    except Exception as e:
        logger.error(f"Erro ao criar índices: {e}")
        return False


def validate_dw(engine: Engine) -> bool:
    """
    Valida a integridade do Data Warehouse criado.

    Args:
        engine: Engine do SQLAlchemy

    Returns:
        True se validação passou
    """
    try:
        with engine.connect() as conn:
            # Verificar se tabelas existem
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "ORDER BY name"
            ))
            tables = [row[0] for row in result]

            required_tables = [
                "fato_incidentes_operacionais",
                "dim_area", "dim_system", "dim_date"
            ]

            for table in required_tables:
                if table not in tables:
                    logger.error(f"Tabela obrigatória não encontrada: {table}")
                    return False

            # Contar registros
            for table in required_tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                logger.info(f"  Tabela '{table}': {count} registros")

        logger.info("✓ Validação do DW passou com sucesso")
        return True

    except Exception as e:
        logger.error(f"Erro ao validar DW: {e}")
        return False


def main() -> None:
    """Função principal do módulo de carga."""
    logger.info("=" * 60)
    logger.info("Iniciando Etapa 3: CARGA")
    logger.info("=" * 60)

    # Conectar
    engine = create_engine_connection(DB_PATH)
    if engine is None:
        logger.error("❌ Falha ao conectar ao banco de dados")
        exit(1)

    # Carregar
    df = load_clean_data(INPUT_FILE)
    if df is None:
        logger.error("❌ Falha ao carregar dados")
        exit(1)

    # Criar tabelas
    success = True
    success &= create_dimension_area(df, engine)
    success &= create_dimension_system(df, engine)
    success &= create_dimension_date(df, engine)
    success &= create_fact_table(df, engine)

    if not success:
        logger.error("❌ Falha ao criar tabelas")
        exit(1)

    # Otimizar
    if not create_indexes(engine):
        logger.warning("⚠️  Falha ao criar índices")

    # Validar
    if validate_dw(engine):
        logger.info("✅ Carga finalizada com sucesso!")
        exit(0)
    else:
        logger.error("❌ Validação do DW falhou")
        exit(1)


if __name__ == "__main__":
    main()
