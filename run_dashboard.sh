#!/bin/bash
# Script para iniciar o Dashboard Streamlit

echo "🌐 Iniciando Dashboard de Risco Operacional..."
echo "================================================"
echo ""
echo "📍 Abrindo em: http://localhost:8501"
echo ""
echo "💡 Dicas:"
echo "  • Use os filtros na barra lateral para customizar"
echo "  • Passe o mouse sobre os gráficos para detalhes"
echo "  • Pressione 'Ctrl+C' para parar o servidor"
echo ""
echo "================================================"
echo ""

# Ativar ambiente virtual se não estiver ativado
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Ativando ambiente virtual..."
    source .venv/bin/activate
fi

# Iniciar Streamlit
.venv/bin/streamlit run dashboards/streamlit_app.py
