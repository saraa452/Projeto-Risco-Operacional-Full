"""
Módulo de Extração - ETL Pipeline

Responsável pela extração de arquivos CSV de dados de incidentes operacionais
e perdas mensais, copiando-os para a pasta de trabalho do projeto.

Típo de execução:
    python etl/extracao.py
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Optional

# Adicionar diretório raiz ao path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))

import config

logger = config.get_logger(__name__)

# Configurações de origem (essas podem vir de variáveis de ambiente)
# Tenta caminhos alternativos se o padrão não existir
DEFAULT_INCIDENTES = "/mnt/data/incidentes_operacionais.csv"
DEFAULT_PERDAS = "/mnt/data/perdas_mensais_por_area.csv"
FALLBACK_INCIDENTES = config.DATA_DIR / "incidentes_operacionais.csv"
FALLBACK_PERDAS = config.DATA_DIR / "perdas_mensais_por_area.csv"

SOURCE_INCIDENTES = os.getenv("SOURCE_INCIDENTES", DEFAULT_INCIDENTES)
SOURCE_PERDAS = os.getenv("SOURCE_PERDAS", DEFAULT_PERDAS)

# Se os arquivos padrão não existem, usar fallback local
if not Path(SOURCE_INCIDENTES).exists() and FALLBACK_INCIDENTES.exists():
    SOURCE_INCIDENTES = str(FALLBACK_INCIDENTES)
if not Path(SOURCE_PERDAS).exists() and FALLBACK_PERDAS.exists():
    SOURCE_PERDAS = str(FALLBACK_PERDAS)


def extract_files(
    source_incidentes: str,
    source_perdas: str,
    destination_dir: Path
) -> bool:
    """
    Extrai arquivos CSV de dados brutos para o diretório de trabalho.

    Args:
        source_incidentes: Caminho do arquivo CSV de incidentes
        source_perdas: Caminho do arquivo CSV de perdas mensais
        destination_dir: Diretório de destino

    Returns:
        bool: True se extração bem-sucedida, False caso contrário

    Raises:
        FileNotFoundError: Se os arquivos de origem não existem
        PermissionError: Se não houver permissão de escrita no destino
    """
    try:
        # Garantir que o diretório de destino existe
        destination_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Diretório de destino: {destination_dir}")

        # Validar que os arquivos de origem existem
        source_inc_path = Path(source_incidentes)
        source_perd_path = Path(source_perdas)

        if not source_inc_path.exists():
            raise FileNotFoundError(
                f"Arquivo de incidentes não encontrado: {source_incidentes}"
            )

        if not source_perd_path.exists():
            raise FileNotFoundError(
                f"Arquivo de perdas não encontrado: {source_perdas}"
            )

        # Copiar arquivos com preservação de metadados
        dest_incidentes = destination_dir / "incidentes_operacionais.csv"
        dest_perdas = destination_dir / "perdas_mensais_por_area.csv"

        # Só copiar se não são o mesmo arquivo
        if source_inc_path != dest_incidentes:
            shutil.copy2(source_incidentes, dest_incidentes)
            logger.info(f"✓ Arquivo copiado: {dest_incidentes}")
        else:
            logger.info(f"✓ Arquivo já presente: {dest_incidentes}")

        if source_perd_path != dest_perdas:
            shutil.copy2(source_perdas, dest_perdas)
            logger.info(f"✓ Arquivo copiado: {dest_perdas}")
        else:
            logger.info(f"✓ Arquivo já presente: {dest_perdas}")

        logger.info("Extração concluída com sucesso!")
        return True

    except FileNotFoundError as e:
        logger.error(f"Erro - Arquivo não encontrado: {e}")
        return False
    except PermissionError as e:
        logger.error(f"Erro - Permissão negada: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado durante extração: {e}")
        return False


def main() -> None:
    """Função principal do módulo de extração."""
    logger.info("=" * 60)
    logger.info("Iniciando Etapa 1: EXTRAÇÃO")
    logger.info("=" * 60)

    success = extract_files(
        SOURCE_INCIDENTES,
        SOURCE_PERDAS,
        config.DATA_DIR
    )

    if success:
        logger.info("✅ Extração finalizada com sucesso!")
        exit(0)
    else:
        logger.error("❌ Falha na extração de dados")
        exit(1)


if __name__ == "__main__":
    main()
