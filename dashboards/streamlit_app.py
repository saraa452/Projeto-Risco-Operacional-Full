"""
Dashboard de Análise de Risco Operacional - Streamlit

Interface interativa para visualização de KPIs, tendências e análises
de riscos operacionais bancários.

Execução:
    streamlit run dashboards/streamlit_app.py
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
import config

# ================== CONFIGURAÇÕES STREAMLIT ==================
st.set_page_config(
    page_title="Risco Operacional - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-title {
        color: #1f77b4;
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .metric-value {
        color: #262730;
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ================== CACHE E DADOS ==================
@st.cache_resource
def get_db_engine():
    """Conectar ao banco de dados (cached)."""
    return create_engine(config.DATABASE_URL)

@st.cache_data(ttl=3600)
def load_data():
    """Carregar dados da tabela fato (cached por 1 hora)."""
    try:
        engine = get_db_engine()
        df = pd.read_sql_table("fato_incidentes_operacionais", engine)
        df["datetime"] = pd.to_datetime(df["datetime"])
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None

@st.cache_data
def load_dimensions():
    """Carregar dimensões do banco de dados."""
    engine = get_db_engine()
    try:
        dim_area = pd.read_sql_table("dim_area", engine)
        dim_system = pd.read_sql_table("dim_system", engine)
        dim_date = pd.read_sql_table("dim_date", engine)
        return dim_area, dim_system, dim_date
    except Exception as e:
        st.warning(f"⚠️  Erro ao carregar dimensões: {e}")
        return None, None, None

# ================== FUNÇÕES DE CÁLCULO ==================
def calculate_kpis(df_filtered):
    """Calcula KPIs principais."""
    return {
        "total_incidents": len(df_filtered),
        "total_loss": df_filtered["impact_brl"].sum(),
        "avg_loss": df_filtered["impact_brl"].mean(),
        "max_loss": df_filtered["impact_brl"].max(),
        "avg_duration": df_filtered["duration_minutes"].mean(),
        "critical_count": len(df_filtered[df_filtered["severity"] == "Crítica"]),
        "high_count": len(df_filtered[df_filtered["severity"] == "Alta"]),
    }

def get_top_areas(df_filtered, n=10):
    """Top N áreas por perda."""
    return df_filtered.groupby("area")["impact_brl"].sum().sort_values(ascending=False).head(n)

def get_top_systems(df_filtered, n=10):
    """Top N sistemas por impacto."""
    return df_filtered.groupby("system")["impact_brl"].sum().sort_values(ascending=False).head(n)

# ================== GRÁFICOS ==================
def create_kpi_metrics(kpis):
    """Cria cards de KPIs."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total de Incidentes",
            f"{kpis['total_incidents']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            "💰 Perdas Totais (R$)",
            f"{kpis['total_loss']:,.2f}",
            delta=f"Média: {kpis['avg_loss']:,.2f}"
        )
    
    with col3:
        st.metric(
            "🚨 Críticos",
            f"{int(kpis['critical_count'])}",
            delta=f"Altos: {int(kpis['high_count'])}"
        )
    
    with col4:
        st.metric(
            "⏱️ MTTR Médio (min)",
            f"{kpis['avg_duration']:.0f}",
            delta=None
        )

def plot_monthly_losses(df_filtered):
    """Gráfico de perdas por mês."""
    monthly_data = (
        df_filtered.groupby("year_month")["impact_brl"]
        .sum()
        .reset_index()
        .sort_values("year_month")
    )
    
    fig = px.bar(
        monthly_data,
        x="year_month",
        y="impact_brl",
        title="Perdas Operacionais por Mês",
        labels={"year_month": "Período", "impact_brl": "Perdas (R$)"},
        color="impact_brl",
        color_continuous_scale="Reds"
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        hovermode="x unified"
    )
    
    return fig

def plot_severity_distribution(df_filtered):
    """Gráfico de distribuição de severidade."""
    severity_order = ["Baixa", "Média", "Alta", "Crítica"]
    severity_data = (
        df_filtered["severity"]
        .value_counts()
        .reindex(severity_order)
    )
    
    colors = {
        "Baixa": "#2ecc71",
        "Média": "#f39c12",
        "Alta": "#e74c3c",
        "Crítica": "#c0392b"
    }
    
    fig = px.pie(
        values=severity_data.values,
        names=severity_data.index,
        title="Distribuição de Severidade",
        color=severity_data.index,
        color_discrete_map=colors
    )
    
    fig.update_layout(height=400)
    return fig

def plot_top_areas(df_filtered, n=10):
    """Gráfico de top áreas por perda."""
    top_areas = get_top_areas(df_filtered, n)
    
    fig = px.bar(
        x=top_areas.values,
        y=top_areas.index,
        orientation="h",
        title=f"Top {n} Áreas por Perdas",
        labels={"x": "Perdas (R$)", "y": "Área"},
        color=top_areas.values,
        color_continuous_scale="Oranges"
    )
    
    fig.update_layout(height=400)
    return fig

def plot_top_systems(df_filtered, n=10):
    """Gráfico de top sistemas por impacto."""
    top_systems = get_top_systems(df_filtered, n)
    
    fig = px.bar(
        x=top_systems.values,
        y=top_systems.index,
        orientation="h",
        title=f"Top {n} Sistemas por Impacto",
        labels={"x": "Impacto (R$)", "y": "Sistema"},
        color=top_systems.values,
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(height=400)
    return fig

def plot_incidents_by_area(df_filtered):
    """Gráfico de incidentes por área."""
    area_counts = df_filtered.groupby("area").size().sort_values(ascending=True)
    
    fig = px.bar(
        x=area_counts.values,
        y=area_counts.index,
        orientation="h",
        title="Quantidade de Incidentes por Área",
        labels={"x": "Quantidade", "y": "Área"},
        color=area_counts.values,
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(height=300)
    return fig

def plot_duration_vs_impact(df_filtered):
    """Scatter plot: Duração vs Impacto."""
    fig = px.scatter(
        df_filtered.sample(min(500, len(df_filtered))),
        x="duration_minutes",
        y="impact_brl",
        color="severity",
        size="impact_brl",
        hover_data=["area", "system"],
        title="Duração vs Impacto Financeiro",
        labels={"duration_minutes": "Duração (min)", "impact_brl": "Impacto (R$)"},
        color_discrete_map={
            "Baixa": "#2ecc71",
            "Média": "#f39c12",
            "Alta": "#e74c3c",
            "Crítica": "#c0392b"
        }
    )
    
    fig.update_layout(height=400)
    return fig

def plot_incidents_timeline(df_filtered):
    """Gráfico de timeline de incidentes."""
    daily_incidents = (
        df_filtered.groupby(df_filtered["datetime"].dt.date)
        .size()
        .reset_index()
    )
    daily_incidents.columns = ["date", "count"]
    
    fig = px.line(
        daily_incidents,
        x="date",
        y="count",
        title="Timeline de Incidentes (Diário)",
        labels={"date": "Data", "count": "Quantidade"},
        markers=True
    )
    
    fig.update_layout(height=300, hovermode="x unified")
    return fig

# ================== SIDEBAR - FILTROS ==================
st.sidebar.title("🔧 Filtros")

df_full = load_data()

if df_full is not None:
    # Período
    min_date = df_full["datetime"].min().date()
    max_date = df_full["datetime"].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Áreas
    areas = st.sidebar.multiselect(
        "🏢 Áreas",
        options=sorted(df_full["area"].unique()),
        default=sorted(df_full["area"].unique())
    )
    
    # Severidade
    severities = st.sidebar.multiselect(
        "🚨 Severidade",
        options=["Baixa", "Média", "Alta", "Crítica"],
        default=["Baixa", "Média", "Alta", "Crítica"]
    )
    
    # Sistemas
    systems = st.sidebar.multiselect(
        "💻 Sistemas",
        options=sorted(df_full["system"].unique()),
        default=sorted(df_full["system"].unique())
    )
    
    # Aplicar filtros
    df_filtered = df_full[
        (df_full["datetime"].dt.date >= date_range[0]) &
        (df_full["datetime"].dt.date <= date_range[1]) &
        (df_full["area"].isin(areas)) &
        (df_full["severity"].isin(severities)) &
        (df_full["system"].isin(systems))
    ]
    
    # ================== MAIN CONTENT ==================
    st.title("📊 Dashboard de Risco Operacional")
    st.markdown(f"**Período selecionado**: {date_range[0]} a {date_range[1]} | **Registros**: {len(df_filtered):,}")
    
    # KPIs
    st.markdown("---")
    st.subheader("📈 KPIs Principais")
    kpis = calculate_kpis(df_filtered)
    create_kpi_metrics(kpis)
    
    # Gráficos principais
    st.markdown("---")
    st.subheader("📉 Análise de Tendências")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_monthly_losses(df_filtered), use_container_width=True)
    with col2:
        st.plotly_chart(plot_severity_distribution(df_filtered), use_container_width=True)
    
    # Top Areas e Sistemas
    st.markdown("---")
    st.subheader("🏆 Ranking de Riscos")
    
    col1, col2 = st.columns(2)
    with col1:
        n_areas = st.slider("Mostrar top N áreas", 5, 20, 10, key="areas_slider")
        st.plotly_chart(plot_top_areas(df_filtered, n_areas), use_container_width=True)
    
    with col2:
        n_systems = st.slider("Mostrar top N sistemas", 5, 20, 10, key="systems_slider")
        st.plotly_chart(plot_top_systems(df_filtered, n_systems), use_container_width=True)
    
    # Análises adicionais
    st.markdown("---")
    st.subheader("🔍 Análises Adicionais")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_incidents_by_area(df_filtered), use_container_width=True)
    with col2:
        st.plotly_chart(plot_incidents_timeline(df_filtered), use_container_width=True)
    
    # Scatter plot
    st.markdown("---")
    st.plotly_chart(plot_duration_vs_impact(df_filtered), use_container_width=True)
    
    # Tabela de detalhes
    st.markdown("---")
    st.subheader("📋 Detalhes dos Incidentes")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔎 Buscar por área ou sistema")
    with col2:
        show_rows = st.number_input("Linhas para mostrar", 10, 100, 20)
    
    if search_term:
        df_search = df_filtered[
            (df_filtered["area"].str.contains(search_term, case=False, na=False)) |
            (df_filtered["system"].str.contains(search_term, case=False, na=False))
        ]
    else:
        df_search = df_filtered
    
    # Preparar tabela para exibição
    display_df = df_search[
        ["datetime", "area", "system", "severity", "duration_minutes", "impact_brl", "status"]
    ].sort_values("datetime", ascending=False).head(show_rows)
    
    display_df = display_df.rename(columns={
        "datetime": "Data/Hora",
        "area": "Área",
        "system": "Sistema",
        "severity": "Severidade",
        "duration_minutes": "Duração (min)",
        "impact_brl": "Impacto (R$)",
        "status": "Status"
    })
    
    st.dataframe(
        display_df.style.format({
            "Duração (min)": "{:.0f}",
            "Impacto (R$)": "R$ {:.2f}"
        }),
        use_container_width=True,
        height=400
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">
    🔄 Dashboard de Risco Operacional | Dados atualizados automaticamente a cada hora
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Não foi possível carregar os dados. Execute o pipeline ETL primeiro.")
    st.info("💡 Execute: `make run-etl` no terminal")
