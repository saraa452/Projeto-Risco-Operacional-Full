"""
Módulo de Análise Principal - Risco Operacional

Executa análises principais do Data Warehouse:
- Cálculo de KPIs
- Análise de tendências
- Identificação de áreas de risco
- Geração de visualizações

Típo de execução:
    python analise/risco_operacional_analysis.py
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

# Adicionar diretório raiz ao path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

import config

logger = config.get_logger(__name__)

# Configurações de visualização
plt.style.use("seaborn-v0_8-darkgrid")
COLORS = config.COLORS

# Banco de dados
ENGINE = create_engine(config.DATABASE_URL)


def load_data() -> Optional[pd.DataFrame]:
    """
    Carrega dados da tabela fato.

    Returns:
        DataFrame com dados ou None se erro
    """
    try:
        df = pd.read_sql_table("fato_incidentes_operacionais", ENGINE)
        df["datetime"] = pd.to_datetime(df["datetime"])
        logger.info(f"✓ Dados carregados: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return None


def calculate_monthly_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula KPIs do mês mais recente.

    Args:
        df: DataFrame com dados

    Returns:
        Dicionário com KPIs
    """
    try:
        recent_month = df["year_month"].max()
        df_recent = df[df["year_month"] == recent_month]

        kpis = {
            "total_incidents": len(df_recent),
            "total_loss_brl": df_recent["impact_brl"].sum(),
            "avg_loss_brl": df_recent["impact_brl"].mean(),
            "max_loss_brl": df_recent["impact_brl"].max(),
            "avg_duration_min": df_recent["duration_minutes"].mean(),
            "critical_count": len(df_recent[df_recent["severity"] == "Crítica"]),
            "significant_loss_count": df_recent["significant_loss"].sum()
        }

        logger.info(f"KPIs calculados para período: {recent_month}")
        return kpis

    except Exception as e:
        logger.error(f"Erro ao calcular KPIs: {e}")
        return {}


def print_kpis(df: pd.DataFrame) -> None:
    """
    Exibe KPIs no console de forma formatada.

    Args:
        df: DataFrame com dados
    """
    kpis = calculate_monthly_kpis(df)

    if not kpis:
        return

    print("\n" + "=" * 60)
    print("📊 KPIs - MÊS MAIS RECENTE")
    print("=" * 60)
    print(f"Total de incidentes: {kpis['total_incidents']}")
    print(f"Perdas totais (R$): {kpis['total_loss_brl']:,.2f}")
    print(f"Perda média (R$): {kpis['avg_loss_brl']:,.2f}")
    print(f"Perda máxima (R$): {kpis['max_loss_brl']:,.2f}")
    print(f"Duração média (min): {kpis['avg_duration_min']:.2f}")
    print(f"Incidentes críticos: {int(kpis['critical_count'])}")
    print(f"Perdas significativas: {int(kpis['significant_loss_count'])}")
    print("=" * 60)


def get_top_areas_by_loss(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """
    Identifica áreas com maiores perdas.

    Args:
        df: DataFrame com dados
        top_n: Top N áreas

    Returns:
        Series com ranking de áreas
    """
    try:
        top_areas = df.groupby("area")["impact_brl"].sum().sort_values(ascending=False).head(top_n)
        logger.info(f"Top {top_n} áreas por perda calculado")
        return top_areas
    except Exception as e:
        logger.error(f"Erro ao calcular top áreas: {e}")
        return pd.Series()


def generate_monthly_loss_plot(df: pd.DataFrame, output_dir: Path) -> bool:
    """
    Gera gráfico de perdas por mês.

    Args:
        df: DataFrame com dados
        output_dir: Diretório de saída

    Returns:
        True se bem-sucedido
    """
    try:
        plt.figure(figsize=(12, 6))

        monthly_loss = df.groupby("year_month")["impact_brl"].sum().sort_index()
        monthly_loss.plot(kind="bar", color=COLORS["primary"], alpha=0.8)

        plt.title("Perdas Operacionais por Mês", fontsize=14, fontweight="bold")
        plt.xlabel("Período", fontsize=12)
        plt.ylabel("Perdas (R$)", fontsize=12)
        plt.tight_layout()
        plt.xticks(rotation=45)

        filepath = output_dir / "perdas_por_mes.png"
        plt.savefig(filepath, dpi=config.PLOT_DPI)
        plt.close()

        logger.info(f"✓ Gráfico salvo: {filepath}")
        return True

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico de perdas mensal: {e}")
        return False


def generate_severity_distribution_plot(df: pd.DataFrame, output_dir: Path) -> bool:
    """
    Gera gráfico de distribuição de severidade.

    Args:
        df: DataFrame com dados
        output_dir: Diretório de saída

    Returns:
        True se bem-sucedido
    """
    try:
        plt.figure(figsize=(10, 6))

        severity_counts = df["severity"].value_counts()
        colors_list = [COLORS.get(s.lower(), COLORS["primary"]) for s in severity_counts.index]

        severity_counts.plot(kind="bar", color=colors_list, alpha=0.8)

        plt.title("Distribuição de Severidade", fontsize=14, fontweight="bold")
        plt.xlabel("Severidade", fontsize=12)
        plt.ylabel("Quantidade", fontsize=12)
        plt.tight_layout()
        plt.xticks(rotation=45)

        filepath = output_dir / "distribuicao_severidade.png"
        plt.savefig(filepath, dpi=config.PLOT_DPI)
        plt.close()

        logger.info(f"✓ Gráfico salvo: {filepath}")
        return True

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico de severidade: {e}")
        return False


def generate_top_areas_plot(df: pd.DataFrame, output_dir: Path) -> bool:
    """
    Gera gráfico de top áreas por perda.

    Args:
        df: DataFrame com dados
        output_dir: Diretório de saída

    Returns:
        True se bem-sucedido
    """
    try:
        plt.figure(figsize=(12, 8))

        top_areas = get_top_areas_by_loss(df, top_n=10)
        top_areas.plot(kind="barh", color=COLORS["secondary"], alpha=0.8)

        plt.title("Top 10 Áreas por Perdas Totais", fontsize=14, fontweight="bold")
        plt.xlabel("Perdas (R$)", fontsize=12)
        plt.ylabel("Área", fontsize=12)
        plt.tight_layout()

        filepath = output_dir / "top_areas_perdas.png"
        plt.savefig(filepath, dpi=config.PLOT_DPI)
        plt.close()

        logger.info(f"✓ Gráfico salvo: {filepath}")
        return True

    except Exception as e:
        logger.error(f"Erro ao gerar gráfico de top áreas: {e}")
        return False


def print_summary(df: pd.DataFrame) -> None:
    """
    Imprime resumo executivo dos dados.

    Args:
        df: DataFrame com dados
    """
    print("\n" + "=" * 60)
    print("📋 RESUMO EXECUTIVO")
    print("=" * 60)
    print(f"Período analisado: {df['year_month'].min()} a {df['year_month'].max()}")
    print(f"Total de incidentes: {len(df):,}")
    print(f"Total de perdas: R$ {df['impact_brl'].sum():,.2f}")
    print(f"Perda média por incidente: R$ {df['impact_brl'].mean():,.2f}")
    print(f"Áreas afetadas: {df['area'].nunique()}")
    print(f"Sistemas afetados: {df['system'].nunique()}")

    print("\n🔴 Top 5 Áreas por Perda:")
    top_5 = get_top_areas_by_loss(df, top_n=5)
    for area, loss in top_5.items():
        print(f"  • {area}: R$ {loss:,.2f}")

    print("=" * 60)


def main() -> None:
    """Função principal do módulo de análise."""
    logger.info("=" * 60)
    logger.info("Iniciando ANÁLISE DE RISCO OPERACIONAL")
    logger.info("=" * 60)

    # Carregar dados
    df = load_data()
    if df is None or len(df) == 0:
        logger.error("❌ Nenhum dado disponível para análise")
        exit(1)

    # Exibir resumo
    print_summary(df)
    print_kpis(df)

    # Gerar visualizações
    success = True
    success &= generate_monthly_loss_plot(df, config.PLOTS_DIR)
    success &= generate_severity_distribution_plot(df, config.PLOTS_DIR)
    success &= generate_top_areas_plot(df, config.PLOTS_DIR)

    if success:
        logger.info("✅ Análise concluída com sucesso!")
        logger.info(f"Gráficos salvos em: {config.PLOTS_DIR}")
        exit(0)
    else:
        logger.error("❌ Falha em alguma das análises")
        exit(1)


if __name__ == "__main__":
    main()


# Heatmap hora x dia (precisa agrupar por hora e dayofweek)
df['hour'] = pd.to_datetime(df['datetime']).dt.hour
df['dow'] = pd.to_datetime(df['datetime']).dt.dayofweek
pivot = df.pivot_table(index='hour', columns='dow', values='incident_id', aggfunc='count').fillna(0)
plt.figure(figsize=(10,6))
plt.imshow(pivot, aspect='auto')
plt.colorbar()
plt.title('Mapa de calor: incidentes por hora x dia da semana')
plt.xlabel('Dia da semana (0=Segunda)')
plt.ylabel('Hora do dia')
plt.savefig(os.path.join(BASE_DIR, 'plots', 'heatmap_hora_dow.png'))
print('Plot salvo: plots/heatmap_hora_dow.png')
