"""
Módulo de Tratamento - ETL Pipeline

Responsável pela limpeza, validação e enriquecimento dos dados brutos:
- Remove duplicados
- Corrige e valida tipos de dados
- Normaliza valores
- Cria colunas auxiliares
- Exporta dados para a etapa de carga

Típo de execução:
    python etl/tratamento.py
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Adicionar diretório raiz ao path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np

import config

logger = config.get_logger(__name__)

# Configurações
INPUT_FILE = config.DATA_DIR / "incidentes_operacionais.csv"
OUTPUT_DIR = config.DATA_DIR / "clean"
OUTPUT_FILE = OUTPUT_DIR / "incidentes_operacionais_clean.csv"

# Colunas esperadas
REQUIRED_COLUMNS = [
    "incident_id", "datetime", "date", "time", "area", "system",
    "type_incident", "duration_minutes", "impact_brl", "severity",
    "status", "recurrence_count", "customer_id", "latitude", "longitude"
]

# Mapeamento de severidades válidas
VALID_SEVERITIES = ["Baixa", "Média", "Alta", "Crítica"]


def load_raw_data(filepath: Path) -> Optional[pd.DataFrame]:
    """
    Carrega dados brutos do CSV.

    Args:
        filepath: Caminho do arquivo CSV

    Returns:
        DataFrame carregado ou None se erro

    Raises:
        FileNotFoundError: Se arquivo não existe
    """
    try:
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

        df = pd.read_csv(filepath, parse_dates=["datetime"])
        logger.info(f"✓ Arquivo carregado com {len(df)} linhas e {len(df.columns)} colunas")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return None


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove registros duplicados mantendo o primeiro.

    Args:
        df: DataFrame original

    Returns:
        DataFrame sem duplicatas
    """
    initial_rows = len(df)
    df = df.drop_duplicates(subset=["incident_id"], keep="first")
    removed = initial_rows - len(df)

    if removed > 0:
        logger.info(f"✓ Removidas {removed} linhas duplicadas")

    return df


def clean_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige e valida tipos de dados.

    Args:
        df: DataFrame para limpeza

    Returns:
        DataFrame com tipos corrigidos
    """
    numeric_columns = ["duration_minutes", "impact_brl", "recurrence_count"]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            logger.debug(f"Column '{col}' convertida para numeric")

    # Validar severidade
    if "severity" in df.columns:
        mask = ~df["severity"].isin(VALID_SEVERITIES)
        if mask.any():
            logger.warning(f"Encontradas {mask.sum()} severidades inválidas. Substituindo por 'Baixa'")
            df.loc[mask, "severity"] = "Baixa"

    logger.info("✓ Tipos de dados validados e corrigidos")
    return df


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza colunas de texto (trim, title case).

    Args:
        df: DataFrame para normalização

    Returns:
        DataFrame normalizado
    """
    text_columns = ["area", "system", "type_incident", "status"]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    logger.info("✓ Colunas de texto normalizadas")
    return df


def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece dados com colunas derivadas.

    Args:
        df: DataFrame para enriquecimento

    Returns:
        DataFrame enriquecido
    """
    # Coluna year_month
    if "datetime" in df.columns:
        df["year_month"] = df["datetime"].dt.to_period("M").astype(str)

    # Flag de perda significativa (top 10%)
    if "impact_brl" in df.columns:
        threshold = df["impact_brl"].quantile(0.90)
        df["significant_loss"] = (df["impact_brl"] > threshold).astype(int)
        logger.info(f"✓ Criada flag de perda significativa (limiar: R$ {threshold:,.2f})")

    # Mês e Ano separados
    if "datetime" in df.columns:
        df["month"] = df["datetime"].dt.month
        df["year"] = df["datetime"].dt.year

    logger.info("✓ Dados enriquecidos com colunas derivadas")
    return df


def validate_data(df: pd.DataFrame) -> bool:
    """
    Valida a qualidade dos dados processados.

    Args:
        df: DataFrame para validação

    Returns:
        True se validação passou, False caso contrário
    """
    issues = []

    # Verificar valores nulos críticos
    critical_columns = ["incident_id", "impact_brl", "area"]
    for col in critical_columns:
        if col in df.columns and df[col].isnull().any():
            issues.append(f"Coluna '{col}' contém valores nulos")

    # Verificar valores negativos
    if "impact_brl" in df.columns and (df["impact_brl"] < 0).any():
        issues.append("Coluna 'impact_brl' contém valores negativos")

    if issues:
        for issue in issues:
            logger.warning(f"⚠️  {issue}")
        return False

    logger.info("✓ Validação de dados passou com sucesso")
    return True


def save_clean_data(df: pd.DataFrame, filepath: Path) -> bool:
    """
    Salva dados limpos para próxima etapa.

    Args:
        df: DataFrame para salvar
        filepath: Caminho de destino

    Returns:
        True se salvamento bem-sucedido
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
        logger.info(f"✓ Dados limpos salvos em: {filepath}")
        logger.info(f"  Total de linhas: {len(df)}")
        logger.info(f"  Total de colunas: {len(df.columns)}")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        return False


def main() -> None:
    """Função principal do módulo de tratamento."""
    logger.info("=" * 60)
    logger.info("Iniciando Etapa 2: TRATAMENTO")
    logger.info("=" * 60)

    # Carregar
    df = load_raw_data(INPUT_FILE)
    if df is None:
        logger.error("❌ Falha ao carregar dados")
        exit(1)

    # Limpar
    df = remove_duplicates(df)
    df = clean_data_types(df)
    df = normalize_text_columns(df)
    df = enrich_data(df)

    # Validar
    if not validate_data(df):
        logger.warning("⚠️  Dados com problemas de validação, mas continuando...")

    # Salvar
    if save_clean_data(df, OUTPUT_FILE):
        logger.info("✅ Tratamento finalizado com sucesso!")
        exit(0)
    else:
        logger.error("❌ Falha ao salvar dados tratados")
        exit(1)


if __name__ == "__main__":
    main()
